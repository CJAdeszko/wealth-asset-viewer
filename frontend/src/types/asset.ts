export interface Asset {
  wid: string;
  asset_id: string | null;
  cognito_id: string | null;
  nickname: string | null;
  asset_name: string | null;
  asset_description: string | null;
  asset_info_type: string | null;
  wealth_asset_type: string | null;
  primary_asset_category: string | null;
  asset_info: Record<string, unknown> | null;
  balance_current: number | null;
  balance_cost_basis: number | null;
  balance_quantity_current: number | null;
  balance_as_of: string | null;
  balance_from: string | null;
  balance_cost_from: string | null;
  balance_price: number | null;
  balance_price_from: string | null;
  is_active: boolean | null;
  is_asset: boolean | null;
  is_favorite: boolean | null;
  include_in_net_worth: boolean | null;
  has_investment: boolean | null;
  is_linked_vendor: boolean | null;
  institution_id: number | null;
  institution_name: string | null;
  user_institution_id: string | null;
  integration: string | null;
  integration_account_id: string | null;
  asset_owner_name: string | null;
  ownership: string | null;
  beneficiary_composition: string | null;
  vendor_account_type: string | null;
  vendor_container: string | null;
  vendor_response: string | null;
  vendor_response_type: string | null;
  asset_mask: string | null;
  currency_code: string | null;
  description_estate_plan: string | null;
  holdings: string | null;
  logo_name: string | null;
  note: string | null;
  note_date: string | null;
  status: string | null;
  status_code: string | null;
  creation_date: string | null;
  modification_date: string | null;
  last_update: string | null;
  last_update_attempt: string | null;
  next_update: string | null;
  deactivate_by: string | null;
}

export interface AssetListResponse {
  items: Asset[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface GroupedAssets {
  [category: string]: {
    total: number;
    subcategories: {
      [subcategory: string]: {
        total: number;
        assets: Asset[];
      };
    };
  };
}

