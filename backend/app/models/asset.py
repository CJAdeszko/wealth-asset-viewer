import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Asset(Base):
    __tablename__ = "assets"
    
    wid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Core identification fields
    asset_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    cognito_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(255))
    asset_name: Mapped[Optional[str]] = mapped_column(String(255))
    asset_description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Asset type and category
    asset_info_type: Mapped[Optional[str]] = mapped_column(String(100))
    wealth_asset_type: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    primary_asset_category: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Asset info (stored as JSONB for flexibility)
    asset_info: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    # Balance fields
    balance_current: Mapped[Optional[float]] = mapped_column(Float)
    balance_cost_basis: Mapped[Optional[float]] = mapped_column(Float)
    balance_quantity_current: Mapped[Optional[float]] = mapped_column(Float)
    balance_as_of: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    balance_from: Mapped[Optional[str]] = mapped_column(String(100))
    balance_cost_from: Mapped[Optional[str]] = mapped_column(String(100))
    balance_price: Mapped[Optional[float]] = mapped_column(Float)
    balance_price_from: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status flags
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, index=True)
    is_asset: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    is_favorite: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    include_in_net_worth: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
    has_investment: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_linked_vendor: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # Institution fields
    institution_id: Mapped[Optional[int]] = mapped_column()
    institution_name: Mapped[Optional[str]] = mapped_column(String(255))
    user_institution_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Integration fields
    integration: Mapped[Optional[str]] = mapped_column(String(255))
    integration_account_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Owner fields
    asset_owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    ownership: Mapped[Optional[str]] = mapped_column(Text)
    beneficiary_composition: Mapped[Optional[str]] = mapped_column(Text)
    
    # Vendor fields
    vendor_account_type: Mapped[Optional[str]] = mapped_column(String(100))
    vendor_container: Mapped[Optional[str]] = mapped_column(String(100))
    vendor_response: Mapped[Optional[str]] = mapped_column(Text)
    vendor_response_type: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Additional metadata
    asset_mask: Mapped[Optional[str]] = mapped_column(String(50))
    currency_code: Mapped[Optional[str]] = mapped_column(String(10))
    description_estate_plan: Mapped[Optional[str]] = mapped_column(Text)
    holdings: Mapped[Optional[str]] = mapped_column(Text)
    logo_name: Mapped[Optional[str]] = mapped_column(String(255))
    note: Mapped[Optional[str]] = mapped_column(Text)
    note_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]] = mapped_column(String(100))
    status_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Timestamps
    creation_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    modification_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_update_attempt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_update: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    deactivate_by: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    def __repr__(self) -> str:
        return f"<Asset(wid={self.wid}, nickname={self.nickname}, type={self.wealth_asset_type})>"

