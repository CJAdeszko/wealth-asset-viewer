import type { Asset, AssetListResponse } from '../types/asset';

const API_BASE = '/api/v1';

export async function fetchAssets(params?: {
  page?: number;
  page_size?: number;
  wealth_asset_type?: string;
  primary_asset_category?: string;
  is_active?: boolean;
}): Promise<AssetListResponse> {
  const searchParams = new URLSearchParams();
  
  if (params?.page) searchParams.set('page', params.page.toString());
  if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
  if (params?.wealth_asset_type) searchParams.set('wealth_asset_type', params.wealth_asset_type);
  if (params?.primary_asset_category) searchParams.set('primary_asset_category', params.primary_asset_category);
  if (params?.is_active !== undefined) searchParams.set('is_active', params.is_active.toString());
  
  const queryString = searchParams.toString();
  const url = `${API_BASE}/assets${queryString ? `?${queryString}` : ''}`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch assets: ${response.statusText}`);
  }
  
  return response.json();
}

export async function fetchAllAssets(): Promise<Asset[]> {
  const allAssets: Asset[] = [];
  let page = 1;
  const pageSize = 100;
  let hasMore = true;
  
  while (hasMore) {
    const response = await fetchAssets({ page, page_size: pageSize });
    allAssets.push(...response.items);
    hasMore = page < response.pages;
    page++;
  }
  
  return allAssets;
}

export async function fetchAsset(wid: string): Promise<Asset> {
  const response = await fetch(`${API_BASE}/assets/${wid}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch asset: ${response.statusText}`);
  }
  
  return response.json();
}

