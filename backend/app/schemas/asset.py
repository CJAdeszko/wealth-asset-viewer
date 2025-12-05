from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    """Base schema with shared asset fields."""
    
    # Core identification fields
    asset_id: Optional[str] = None
    cognito_id: Optional[str] = None
    nickname: Optional[str] = None
    asset_name: Optional[str] = None
    asset_description: Optional[str] = None
    
    # Asset type and category
    asset_info_type: Optional[str] = None
    wealth_asset_type: Optional[str] = None
    primary_asset_category: Optional[str] = None
    
    # Asset info (flexible JSON structure)
    asset_info: Optional[dict[str, Any]] = None
    
    # Balance fields
    balance_current: Optional[float] = None
    balance_cost_basis: Optional[float] = None
    balance_quantity_current: Optional[float] = None
    balance_as_of: Optional[datetime] = None
    balance_from: Optional[str] = None
    balance_cost_from: Optional[str] = None
    balance_price: Optional[float] = None
    balance_price_from: Optional[str] = None
    
    # Status flags
    is_active: Optional[bool] = None
    is_asset: Optional[bool] = None
    is_favorite: Optional[bool] = None
    include_in_net_worth: Optional[bool] = None
    has_investment: Optional[bool] = None
    is_linked_vendor: Optional[bool] = None
    
    # Institution fields
    institution_id: Optional[int] = None
    institution_name: Optional[str] = None
    user_institution_id: Optional[str] = None
    
    # Integration fields
    integration: Optional[str] = None
    integration_account_id: Optional[str] = None
    
    # Owner fields
    asset_owner_name: Optional[str] = None
    ownership: Optional[str] = None
    beneficiary_composition: Optional[str] = None
    
    # Vendor fields
    vendor_account_type: Optional[str] = None
    vendor_container: Optional[str] = None
    vendor_response: Optional[str] = None
    vendor_response_type: Optional[str] = None
    
    # Additional metadata
    asset_mask: Optional[str] = None
    currency_code: Optional[str] = None
    description_estate_plan: Optional[str] = None
    holdings: Optional[str] = None
    logo_name: Optional[str] = None
    note: Optional[str] = None
    note_date: Optional[datetime] = None
    status: Optional[str] = None
    status_code: Optional[str] = None
    
    # Timestamps
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None
    last_update: Optional[datetime] = None
    last_update_attempt: Optional[datetime] = None
    next_update: Optional[datetime] = None
    deactivate_by: Optional[datetime] = None


class AssetResponse(AssetBase):
    """Response schema for a single asset."""
    
    wid: UUID
    
    model_config = ConfigDict(from_attributes=True)


class AssetListResponse(BaseModel):
    """Paginated response schema for listing assets."""
    
    items: list[AssetResponse]
    total: int
    page: int
    page_size: int
    pages: int

