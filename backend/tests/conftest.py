import os
import uuid
from datetime import datetime, timezone
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.asset import Asset

# Use test database URL
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://wealth_user:wealth_password@localhost:5433/wealth_assets_test"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_asset_data() -> dict:
    """Return sample asset data matching the JSON format."""
    return {
        "wid": uuid.uuid4(),
        "asset_id": "qJfnKleFCUW6rlYsKEGiEA",
        "cognito_id": "d92f061e-a6b4-4292-97ab-3fd76d4e3442",
        "nickname": "Cash Test",
        "asset_name": None,
        "asset_description": None,
        "asset_info_type": "ManualCash",
        "wealth_asset_type": "Cash",
        "primary_asset_category": "Cash",
        "asset_info": {
            "nickname": "Cash Test",
            "descriptionEstatePlan": "",
            "estimateValue": 5000,
            "purchaseCost": 0,
            "asOfDate": "2025-03-28T15:55:22+00:00",
            "isFavorite": False
        },
        "balance_current": 5000.0,
        "balance_cost_basis": 0.0,
        "balance_quantity_current": 5000.0,
        "balance_as_of": datetime(2025, 3, 28, 15, 55, 22, tzinfo=timezone.utc),
        "balance_from": "UserManual",
        "balance_cost_from": "UserManual",
        "balance_price": None,
        "balance_price_from": "UserManual",
        "is_active": True,
        "is_asset": True,
        "is_favorite": False,
        "include_in_net_worth": True,
        "institution_id": 101,
        "user_institution_id": "i7zh3OMH4UOEjbj2xuHMkw",
        "vendor_response_type": "Other",
        "creation_date": datetime(2025, 3, 28, 15, 55, 36, tzinfo=timezone.utc),
        "modification_date": datetime(2025, 3, 28, 16, 16, 13, tzinfo=timezone.utc),
        "last_update": datetime(2025, 1, 1, 16, 55, 22, tzinfo=timezone.utc),
        "last_update_attempt": datetime(2025, 3, 28, 16, 16, 13, tzinfo=timezone.utc),
    }


@pytest.fixture
def sample_asset(db: Session, sample_asset_data: dict) -> Asset:
    """Create and return a sample asset in the database."""
    asset = Asset(**sample_asset_data)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@pytest.fixture
def multiple_assets(db: Session) -> list[Asset]:
    """Create multiple assets for testing pagination and filtering."""
    assets_data = [
        {
            "wid": uuid.uuid4(),
            "asset_id": f"asset_{i}",
            "nickname": f"Test Asset {i}",
            "wealth_asset_type": "Cash" if i % 2 == 0 else "Investment",
            "primary_asset_category": "Cash" if i % 2 == 0 else "Retirement",
            "balance_current": 1000.0 * (i + 1),
            "is_active": i < 8,  # First 8 are active, last 2 are inactive
        }
        for i in range(10)
    ]
    
    assets = [Asset(**data) for data in assets_data]
    db.add_all(assets)
    db.commit()
    
    for asset in assets:
        db.refresh(asset)
    
    return assets

