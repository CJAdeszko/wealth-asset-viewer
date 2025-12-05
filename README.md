# Wealth Asset Viewer

A financial asset tracking application with a React frontend, FastAPI backend, and PostgreSQL database.

## Project Structure

```
wealth-asset-viewer/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── utils/          # Utility functions (seeding, etc.)
│   │   ├── config.py       # Application configuration
│   │   ├── database.py     # Database connection setup
│   │   └── main.py         # FastAPI application entry point
│   ├── data/               # Seed data files
│   │   └── assets.json     # Sample asset data for seeding
│   ├── scripts/            # CLI scripts
│   │   └── seed.py         # Database seeding script
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration
├── frontend/               # React/Vite frontend application
│   ├── src/
│   │   ├── api/           # API client functions
│   │   ├── components/    # React components
│   │   ├── types/         # TypeScript interfaces
│   │   ├── utils/         # Utility functions
│   │   └── App.tsx        # Main application component
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Container configuration
├── docker-compose.yml      # Full stack Docker services
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Docker and Docker Compose
- PostgreSQL (provided via Docker)

## Quick Start

### Clone the repo locally

```
git clone git@github.com:CJAdeszko/wealth-asset-viewer.git
```

### Option 1: Run with Docker (Recommended)

Start all services with Docker Compose:

```bash
docker-compose up -d
```

This starts:
- **PostgreSQL database**: `localhost:5432`
- **Backend API**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`

### Option 2: Run Locally for Development

#### 1. Start the Database

```bash
docker-compose up -d db
```

#### 2. Set Up and Run the Backend

```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

#### 3. Set Up and Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Frontend

The React frontend provides a read-only view of financial assets organized in a collapsible hierarchy:

- **Categories** (`primary_asset_category`): Top-level grouping with total balance
- **Subcategories** (`wealth_asset_type`): Second-level grouping with subtotal
- **Assets**: Individual asset entries with balance and details

### Frontend Features

- Collapsible category and subcategory groups
- Real-time balance totals at each level
- Net worth summary
- Conservative, professional financial theme using Tailwind CSS
- Responsive design

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

All endpoints are prefixed with `/api/v1`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/assets` | List all assets with optional filtering and pagination |
| POST | `/api/v1/seed` | Seed the database with data from assets.json |
| GET | `/health` | Health check endpoint |

### Query Parameters

#### List Assets (`GET /api/v1/assets`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number (starts at 1) |
| `page_size` | int | 20 | Items per page (max 100) |
| `wealth_asset_type` | string | - | Filter by asset type (e.g., "Cash", "Investment") |
| `primary_asset_category` | string | - | Filter by category (e.g., "Cash", "Retirement") |
| `is_active` | bool | - | Filter by active status |

## Seeding the Database

You can populate the database with sample asset data using either the CLI script or the API endpoint.

### Seed Data File

Place your asset data in `backend/data/assets.json`. The file should contain an array of asset objects in camelCase format (matching the original JSON structure).

### Option 1: CLI Script

```bash
cd backend
source venv/bin/activate

# Seed from default file (backend/data/assets.json)
python scripts/seed.py

# Seed from a custom file
python scripts/seed.py --file /path/to/your/assets.json
```

### Option 2: API Endpoint

With the backend running, send a POST request:

```bash
curl -X POST http://localhost:8000/api/v1/seed
```

Or use the Swagger UI at http://localhost:8000/docs and click "Try it out" on the POST `/api/v1/seed` endpoint.

### Seed Behavior

- Assets are matched by their `wid` (UUID)
- Existing assets are skipped (not updated)
- The response shows how many assets were inserted vs. skipped

## Running Tests

### Backend Tests

Ensure the test database is running:

```bash
docker-compose up -d db-test
```

Run the tests with pytest:

```bash
cd backend
source venv/bin/activate
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Environment Variables

### Backend

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://wealth_user:wealth_password@localhost:5432/wealth_assets` | Database connection URL |
| `TEST_DATABASE_URL` | `postgresql://wealth_user:wealth_password@localhost:5433/wealth_assets_test` | Test database connection URL |

You can create a `.env` file in the `backend` directory to override these defaults.

## Database Schema

The application uses SQLAlchemy with automatic table creation on startup. The main table is `assets` with the following key fields:

- `wid` (UUID): Primary key
- `asset_id` (string): External asset identifier
- `nickname` (string): User-friendly asset name
- `wealth_asset_type` (string): Type of asset (e.g., Cash, Investment)
- `primary_asset_category` (string): Asset category
- `balance_current` (float): Current balance
- `is_active` (bool): Whether the asset is active
- `asset_info` (JSONB): Flexible JSON field for additional asset data

See `backend/app/models/asset.py` for the complete schema.

## Development

### Backend Code Structure

- **Models** (`app/models/`): SQLAlchemy ORM models defining database tables
- **Schemas** (`app/schemas/`): Pydantic models for request/response validation
- **API** (`app/api/`): FastAPI route handlers with inline database queries
- **Config** (`app/config.py`): Application settings using pydantic-settings
- **Database** (`app/database.py`): SQLAlchemy engine and session configuration

### Frontend Code Structure

- **API** (`src/api/`): Functions to fetch data from the backend
- **Components** (`src/components/`): React components for the UI
- **Types** (`src/types/`): TypeScript interfaces matching backend schemas
- **Utils** (`src/utils/`): Helper functions (e.g., currency formatting)

## Future Enhancements

- [ ] Add write operations (POST, PUT, DELETE) for asset management
- [ ] Implement authentication and authorization
- [ ] Add database migrations with Alembic (if needed)
- [ ] Add frontend tests with Vitest
- [ ] Deploy with Docker containers to cloud provider
