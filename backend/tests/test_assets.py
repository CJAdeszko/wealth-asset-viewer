import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.asset import Asset


class TestListAssets:
    """Tests for GET /api/v1/assets endpoint."""
    
    def test_list_assets_empty(self, client: TestClient):
        """Test listing assets when database is empty."""
        response = client.get("/api/v1/assets")
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert data["pages"] == 1
    
    def test_list_assets_with_data(self, client: TestClient, sample_asset: Asset):
        """Test listing assets with data in database."""
        response = client.get("/api/v1/assets")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["total"] == 1
        assert data["items"][0]["asset_id"] == sample_asset.asset_id
        assert data["items"][0]["nickname"] == sample_asset.nickname
    
    def test_list_assets_pagination(self, client: TestClient, multiple_assets: list[Asset]):
        """Test pagination of asset listing."""
        # First page
        response = client.get("/api/v1/assets?page=1&page_size=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 10
        assert data["page"] == 1
        assert data["page_size"] == 3
        assert data["pages"] == 4
        
        # Second page
        response = client.get("/api/v1/assets?page=2&page_size=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["page"] == 2
        
        # Last page (partial)
        response = client.get("/api/v1/assets?page=4&page_size=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["page"] == 4
    
    def test_list_assets_filter_by_type(self, client: TestClient, multiple_assets: list[Asset]):
        """Test filtering assets by wealth_asset_type."""
        response = client.get("/api/v1/assets?wealth_asset_type=Cash")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        for item in data["items"]:
            assert item["wealth_asset_type"] == "Cash"
    
    def test_list_assets_filter_by_category(self, client: TestClient, multiple_assets: list[Asset]):
        """Test filtering assets by primary_asset_category."""
        response = client.get("/api/v1/assets?primary_asset_category=Retirement")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        for item in data["items"]:
            assert item["primary_asset_category"] == "Retirement"
    
    def test_list_assets_filter_by_active_status(self, client: TestClient, multiple_assets: list[Asset]):
        """Test filtering assets by is_active status."""
        # Filter active assets
        response = client.get("/api/v1/assets?is_active=true")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8
        
        # Filter inactive assets
        response = client.get("/api/v1/assets?is_active=false")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
    
    def test_list_assets_combined_filters(self, client: TestClient, multiple_assets: list[Asset]):
        """Test combining multiple filters."""
        response = client.get("/api/v1/assets?wealth_asset_type=Cash&is_active=true")
        
        assert response.status_code == 200
        data = response.json()
        # Cash assets are at indices 0, 2, 4, 6, 8; indices 0-7 are active
        # So active Cash assets are at indices 0, 2, 4, 6 = 4 assets
        assert data["total"] == 4
        for item in data["items"]:
            assert item["wealth_asset_type"] == "Cash"
            assert item["is_active"] is True


class TestGetAsset:
    """Tests for GET /api/v1/assets/{wid} endpoint."""
    
    def test_get_asset_found(self, client: TestClient, sample_asset: Asset):
        """Test getting an existing asset by wid."""
        response = client.get(f"/api/v1/assets/{sample_asset.wid}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["wid"] == str(sample_asset.wid)
        assert data["asset_id"] == sample_asset.asset_id
        assert data["nickname"] == sample_asset.nickname
        assert data["wealth_asset_type"] == sample_asset.wealth_asset_type
        assert data["balance_current"] == sample_asset.balance_current
    
    def test_get_asset_not_found(self, client: TestClient):
        """Test getting a non-existent asset."""
        non_existent_wid = uuid.uuid4()
        response = client.get(f"/api/v1/assets/{non_existent_wid}")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Asset not found"
    
    def test_get_asset_invalid_uuid(self, client: TestClient):
        """Test getting an asset with invalid UUID format."""
        response = client.get("/api/v1/assets/invalid-uuid")
        
        assert response.status_code == 422


class TestHealthCheck:
    """Tests for GET /health endpoint."""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

