"""FastAPI application for autonomous month-end close."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import init_db
from backend.routers import (
    transactions_router,
    accruals_router,
    reconciliation_router
)

# Initialize FastAPI app
app = FastAPI(
    title="Month-End Accounting Service",
    description="FastAPI-based backend service supporting autonomous month-end close with zero-touch accounting",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(transactions_router)
app.include_router(accruals_router)
app.include_router(reconciliation_router)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Month-End Accounting Service API",
        "version": "1.0.0",
        "description": "Autonomous month-end close with zero-touch accounting",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "month-end-accounting"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
