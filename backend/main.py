"""FastAPI application for month-end account reconciliation and financial accruals."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.database import init_db
from .routers import transactions, accruals, reconciliation

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Month-End Accounting Service",
    description="""
    FastAPI-based backend service supporting month-end account reconciliation 
    and financial accruals.
    
    ## Features
    
    * **Transaction Management**: Import and track financial transactions
    * **Auto-Reconciliation**: Automatically reconcile low-risk transactions
    * **Accrual Posting**: Post payroll and utilities accruals based on historical data
    * **Month-End Close**: Autonomous month-end close process with approval workflow
    * **Risk Scoring**: Intelligent risk assessment for transactions
    
    ## Workflow
    
    1. Import transactions via `/transactions/import`
    2. Auto-reconcile low-risk items via `/reconciliation/auto`
    3. Post accruals via `/accruals/payroll` and `/accruals/utilities`
    4. Perform month-end close via `/reconciliation/month-end/close`
    5. Check status via `/reconciliation/status`
    """,
    version="1.0.0",
    contact={
        "name": "Accounting Service",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router)
app.include_router(accruals.router)
app.include_router(reconciliation.router)


@app.get("/")
def root():
    """Root endpoint with API information."""
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
