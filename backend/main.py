"""FastAPI application for Month-End Accounting Service."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import init_db
from .routers import transactions_router, accruals_router, reconciliation_router

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Month-End Accounting Service",
    description="FastAPI-based backend service supporting month-end account reconciliation and financial accruals.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(transactions_router)
app.include_router(accruals_router)
app.include_router(reconciliation_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Month-End Accounting Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
