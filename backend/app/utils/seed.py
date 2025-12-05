import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from ..models.asset import Asset


@dataclass
class SeedResult:
    """Result of a seed operation."""
    inserted: int
    skipped: int
    errors: list[str]


def get_seed_data_path() -> Path:
    """Get the path to the seed data file."""
    return Path(__file__).parent.parent.parent / "data" / "assets.json"


def load_seed_data(file_path: Path | None = None) -> list[dict[str, Any]]:
    """
    Load seed data from a JSON file.
    
    Args:
        file_path: Path to the JSON file. Defaults to backend/data/assets.json.
    
    Returns:
        List of asset dictionaries.
    
    Raises:
        FileNotFoundError: If the seed file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    if file_path is None:
        file_path = get_seed_data_path()
    
    with open(file_path, "r") as f:
        return json.load(f)


def parse_datetime(value: str | None) -> datetime | None:
    """Parse an ISO datetime string."""
    if value is None:
        return None
    try:
        # Handle ISO format with timezone
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def parse_asset_info(value: str | None) -> dict | None:
    """Parse the asset_info JSON string."""
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


def convert_to_snake_case(data: dict[str, Any]) -> dict[str, Any]:
    """
    Convert camelCase keys to snake_case for database model compatibility.
    """
    key_mapping = {
        "assetDescription": "asset_description",
        "assetId": "asset_id",
        "assetInfo": "asset_info",
        "assetInfoType": "asset_info_type",
        "assetMask": "asset_mask",
        "assetName": "asset_name",
        "assetOwnerName": "asset_owner_name",
        "balanceAsOf": "balance_as_of",
        "balanceCostBasis": "balance_cost_basis",
        "balanceCostFrom": "balance_cost_from",
        "balanceCurrent": "balance_current",
        "balanceFrom": "balance_from",
        "balancePrice": "balance_price",
        "balancePriceFrom": "balance_price_from",
        "balanceQuantityCurrent": "balance_quantity_current",
        "beneficiaryComposition": "beneficiary_composition",
        "cognitoId": "cognito_id",
        "creationDate": "creation_date",
        "currencyCode": "currency_code",
        "deactivateBy": "deactivate_by",
        "descriptionEstatePlan": "description_estate_plan",
        "hasInvestment": "has_investment",
        "holdings": "holdings",
        "includeInNetWorth": "include_in_net_worth",
        "institutionId": "institution_id",
        "institutionName": "institution_name",
        "integration": "integration",
        "integrationAccountId": "integration_account_id",
        "isActive": "is_active",
        "isAsset": "is_asset",
        "isFavorite": "is_favorite",
        "isLinkedVendor": "is_linked_vendor",
        "lastUpdate": "last_update",
        "lastUpdateAttempt": "last_update_attempt",
        "logoName": "logo_name",
        "modificationDate": "modification_date",
        "nextUpdate": "next_update",
        "nickname": "nickname",
        "note": "note",
        "noteDate": "note_date",
        "ownership": "ownership",
        "primaryAssetCategory": "primary_asset_category",
        "status": "status",
        "statusCode": "status_code",
        "userInstitutionId": "user_institution_id",
        "vendorAccountType": "vendor_account_type",
        "vendorContainer": "vendor_container",
        "vendorResponse": "vendor_response",
        "vendorResponseType": "vendor_response_type",
        "wealthAssetType": "wealth_asset_type",
        "wid": "wid",
    }
    
    converted = {}
    for key, value in data.items():
        snake_key = key_mapping.get(key, key)
        converted[snake_key] = value
    
    return converted


def seed_database(db: Session, data: list[dict[str, Any]] | None = None) -> SeedResult:
    """
    Seed the database with asset data.
    
    Args:
        db: SQLAlchemy database session.
        data: List of asset dictionaries. If None, loads from default file.
    
    Returns:
        SeedResult with counts of inserted, skipped, and any errors.
    """
    if data is None:
        data = load_seed_data()
    
    inserted = 0
    skipped = 0
    errors: list[str] = []
    
    for item in data:
        try:
            # Convert camelCase to snake_case
            converted = convert_to_snake_case(item)
            
            # Check if asset already exists by asset_id
            asset_id = converted.get("asset_id")
            if asset_id:
                existing = db.query(Asset).filter(Asset.asset_id == asset_id).first()
                if existing:
                    skipped += 1
                    continue
            
            # Always generate a new wid (primary key) for each asset
            wid = uuid.uuid4()
            
            # Parse special fields
            asset_info = parse_asset_info(converted.get("asset_info"))
            
            # Convert holdings dict to JSON string if present
            holdings = converted.get("holdings")
            if holdings is not None and isinstance(holdings, dict):
                holdings = json.dumps(holdings)
            
            # Create asset instance
            asset = Asset(
                wid=wid,
                asset_id=converted.get("asset_id"),
                cognito_id=converted.get("cognito_id"),
                nickname=converted.get("nickname"),
                asset_name=converted.get("asset_name"),
                asset_description=converted.get("asset_description"),
                asset_info_type=converted.get("asset_info_type"),
                wealth_asset_type=converted.get("wealth_asset_type"),
                primary_asset_category=converted.get("primary_asset_category"),
                asset_info=asset_info,
                balance_current=converted.get("balance_current"),
                balance_cost_basis=converted.get("balance_cost_basis"),
                balance_quantity_current=converted.get("balance_quantity_current"),
                balance_as_of=parse_datetime(converted.get("balance_as_of")),
                balance_from=converted.get("balance_from"),
                balance_cost_from=converted.get("balance_cost_from"),
                balance_price=converted.get("balance_price"),
                balance_price_from=converted.get("balance_price_from"),
                is_active=converted.get("is_active"),
                is_asset=converted.get("is_asset"),
                is_favorite=converted.get("is_favorite"),
                include_in_net_worth=converted.get("include_in_net_worth"),
                has_investment=converted.get("has_investment"),
                is_linked_vendor=converted.get("is_linked_vendor"),
                institution_id=converted.get("institution_id"),
                institution_name=converted.get("institution_name"),
                user_institution_id=converted.get("user_institution_id"),
                integration=converted.get("integration"),
                integration_account_id=converted.get("integration_account_id"),
                asset_owner_name=converted.get("asset_owner_name"),
                ownership=converted.get("ownership"),
                beneficiary_composition=converted.get("beneficiary_composition"),
                vendor_account_type=converted.get("vendor_account_type"),
                vendor_container=converted.get("vendor_container"),
                vendor_response=converted.get("vendor_response"),
                vendor_response_type=converted.get("vendor_response_type"),
                asset_mask=converted.get("asset_mask"),
                currency_code=converted.get("currency_code"),
                description_estate_plan=converted.get("description_estate_plan"),
                holdings=holdings,
                logo_name=converted.get("logo_name"),
                note=converted.get("note"),
                note_date=parse_datetime(converted.get("note_date")),
                status=converted.get("status"),
                status_code=converted.get("status_code"),
                creation_date=parse_datetime(converted.get("creation_date")),
                modification_date=parse_datetime(converted.get("modification_date")),
                last_update=parse_datetime(converted.get("last_update")),
                last_update_attempt=parse_datetime(converted.get("last_update_attempt")),
                next_update=parse_datetime(converted.get("next_update")),
                deactivate_by=parse_datetime(converted.get("deactivate_by")),
            )
            
            db.add(asset)
            inserted += 1
            
        except Exception as e:
            errors.append(f"Error processing asset: {str(e)}")
    
    # Commit all changes
    if inserted > 0:
        db.commit()
    
    return SeedResult(inserted=inserted, skipped=skipped, errors=errors)

