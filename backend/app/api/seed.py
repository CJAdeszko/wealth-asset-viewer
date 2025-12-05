from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..utils.seed import seed_database, get_seed_data_path

router = APIRouter(prefix="/seed", tags=["seed"])


class SeedResponse(BaseModel):
    """Response model for seed operation."""
    message: str
    inserted: int
    skipped: int
    errors: list[str]


@router.post("", response_model=SeedResponse)
def seed_assets(db: Session = Depends(get_db)) -> SeedResponse:
    """
    Seed the database with asset data from the default seed file.
    
    This endpoint loads assets from `backend/data/assets.json` and inserts
    them into the database. Assets that already exist (by wid) are skipped.
    
    **Note**: This endpoint is intended for development and testing purposes.
    """
    seed_file = get_seed_data_path()
    
    if not seed_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Seed file not found: {seed_file}"
        )
    
    try:
        result = seed_database(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error seeding database: {str(e)}"
        )
    
    if result.inserted > 0:
        message = f"Successfully seeded {result.inserted} assets"
    elif result.skipped > 0:
        message = f"All {result.skipped} assets already exist in the database"
    else:
        message = "No assets were processed"
    
    return SeedResponse(
        message=message,
        inserted=result.inserted,
        skipped=result.skipped,
        errors=result.errors,
    )

