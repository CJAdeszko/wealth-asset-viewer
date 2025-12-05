#!/usr/bin/env python3
"""
CLI script to seed the database with asset data from assets.json.

Usage:
    cd backend
    python scripts/seed.py [--file path/to/assets.json]
"""
import argparse
import sys
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base
from app.utils.seed import load_seed_data, seed_database, get_seed_data_path


def main():
    parser = argparse.ArgumentParser(
        description="Seed the database with asset data from a JSON file."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=None,
        help="Path to the JSON file containing asset data. Defaults to backend/data/assets.json",
    )
    parser.add_argument(
        "--database-url",
        "-d",
        type=str,
        default=None,
        help="Database URL. Defaults to DATABASE_URL environment variable.",
    )
    
    args = parser.parse_args()
    
    # Determine the file path
    file_path = args.file or get_seed_data_path()
    
    if not file_path.exists():
        print(f"Error: Seed file not found: {file_path}")
        sys.exit(1)
    
    # Connect to the database
    database_url = args.database_url or settings.database_url
    print(f"Connecting to database...")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Load and seed data
    print(f"Loading seed data from: {file_path}")
    
    try:
        data = load_seed_data(file_path)
        print(f"Found {len(data)} assets in seed file")
    except Exception as e:
        print(f"Error loading seed data: {e}")
        sys.exit(1)
    
    # Seed the database
    db = SessionLocal()
    try:
        print("Seeding database...")
        result = seed_database(db, data)
        
        print(f"\nSeed completed:")
        print(f"  Inserted: {result.inserted}")
        print(f"  Skipped (already exist): {result.skipped}")
        
        if result.errors:
            print(f"  Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"    - {error}")
        
        if result.inserted > 0:
            print(f"\nSuccessfully seeded {result.inserted} assets!")
        elif result.skipped > 0:
            print(f"\nAll {result.skipped} assets already exist in the database.")
        else:
            print("\nNo assets were processed.")
            
    finally:
        db.close()


if __name__ == "__main__":
    main()

