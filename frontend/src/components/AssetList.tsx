import { useEffect, useState } from 'react';
import type { Asset, GroupedAssets } from '../types/asset';
import { fetchAllAssets } from '../api/assets';
import { formatCurrency } from '../utils/format';
import { CategoryGroup } from './CategoryGroup';

function groupAssets(assets: Asset[]): GroupedAssets {
  const grouped: GroupedAssets = {};
  
  for (const asset of assets) {
    const category = asset.primary_asset_category || 'Other';
    const subcategory = asset.wealth_asset_type || 'Other';
    const balance = asset.balance_current ?? 0;
    
    if (!grouped[category]) {
      grouped[category] = {
        total: 0,
        subcategories: {},
      };
    }
    
    if (!grouped[category].subcategories[subcategory]) {
      grouped[category].subcategories[subcategory] = {
        total: 0,
        assets: [],
      };
    }
    
    grouped[category].total += balance;
    grouped[category].subcategories[subcategory].total += balance;
    grouped[category].subcategories[subcategory].assets.push(asset);
  }
  
  return grouped;
}

export function AssetList() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    async function loadAssets() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchAllAssets();
        setAssets(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load assets');
      } finally {
        setLoading(false);
      }
    }
    
    loadAssets();
  }, []);
  
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex items-center gap-3 text-slate-500">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Loading assets...</span>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        <p className="font-medium">Error loading assets</p>
        <p className="text-sm mt-1">{error}</p>
      </div>
    );
  }
  
  if (assets.length === 0) {
    return (
      <div className="bg-slate-100 border border-slate-200 rounded-lg p-8 text-center text-slate-500">
        <svg
          className="w-12 h-12 mx-auto mb-3 text-slate-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
          />
        </svg>
        <p className="font-medium">No assets found</p>
        <p className="text-sm mt-1">Assets will appear here once they are added.</p>
      </div>
    );
  }
  
  const groupedAssets = groupAssets(assets);
  const totalNetWorth = assets.reduce((sum, asset) => sum + (asset.balance_current ?? 0), 0);
  
  const categoryEntries = Object.entries(groupedAssets).sort(([a], [b]) => 
    (a || 'zzz').localeCompare(b || 'zzz')
  );
  
  return (
    <div>
      <div className="bg-gradient-to-r from-primary-900 to-primary-800 rounded-lg p-6 mb-6 shadow-lg">
        <p className="text-primary-200 text-sm font-medium uppercase tracking-wide">Total Net Worth</p>
        <p className="text-3xl font-bold text-white mt-1">{formatCurrency(totalNetWorth)}</p>
        <p className="text-primary-300 text-sm mt-2">
          {assets.length} {assets.length === 1 ? 'asset' : 'assets'} across {categoryEntries.length} {categoryEntries.length === 1 ? 'category' : 'categories'}
        </p>
      </div>
      
      <div>
        {categoryEntries.map(([categoryName, data]) => (
          <CategoryGroup
            key={categoryName}
            name={categoryName}
            total={data.total}
            subcategories={data.subcategories}
          />
        ))}
      </div>
    </div>
  );
}

