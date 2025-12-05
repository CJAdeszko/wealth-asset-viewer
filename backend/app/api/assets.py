from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.asset import Asset
from ..schemas.asset import AssetListResponse, AssetResponse

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=AssetListResponse)
def list_assets(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    wealth_asset_type: Optional[str] = Query(None, description="Filter by asset type"),
    primary_asset_category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
) -> AssetListResponse:
    """
    List all assets with optional filtering and pagination.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **wealth_asset_type**: Filter by asset type (e.g., "Cash", "Investment")
    - **primary_asset_category**: Filter by category (e.g., "Cash", "Retirement")
    - **is_active**: Filter by active status (true/false)
    """
    query = db.query(Asset)
    
    # Apply filters
    if wealth_asset_type is not None:
        query = query.filter(Asset.wealth_asset_type == wealth_asset_type)
    if primary_asset_category is not None:
        query = query.filter(Asset.primary_asset_category == primary_asset_category)
    if is_active is not None:
        query = query.filter(Asset.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    skip = (page - 1) * page_size
    pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    # Get paginated results
    assets = query.offset(skip).limit(page_size).all()
    
    return AssetListResponse(
        items=assets,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{wid}", response_model=AssetResponse)
def get_asset(
    wid: UUID,
    db: Session = Depends(get_db),
) -> AssetResponse:
    """
    Get a single asset by its wid (UUID).
    
    - **wid**: The unique identifier of the asset
    """
    asset = db.query(Asset).filter(Asset.wid == wid).first()
    
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset

