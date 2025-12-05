from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.assets import router as assets_router
from .api.seed import router as seed_router
from .config import settings
from .database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create database tables
    create_tables()
    yield
    # Shutdown: Nothing to clean up


app = FastAPI(
    title="Wealth Asset Viewer API",
    description="A read-only API for tracking and viewing financial assets",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(assets_router, prefix=settings.api_v1_prefix)
app.include_router(seed_router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

