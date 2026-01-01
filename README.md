# Month-End Accounting Service

FastAPI-based backend service supporting month-end account reconciliation and financial accruals.

## Features

- **Transaction Import**: Bulk import of financial transactions with automatic risk scoring
- **Auto-Reconciliation**: Automatically reconcile low-risk transactions based on configurable thresholds
- **Intelligent Accruals**: Post payroll and utilities accruals based on historical data analysis
- **Autonomous Month-End Close**: End-to-end month-end close process with approval workflow
- **Risk Scoring**: Simplified risk assessment model based on amount, category, and vendor

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. The SQLite database will be automatically created on first run.

## Running the Service

### Development Mode

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python backend/main.py
```

Or use the helper script:

```bash
python run_server.py
```

### Production Mode

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## Quick Test

To quickly test the complete workflow:

```bash
# In one terminal, start the server
python run_server.py

# In another terminal, run the test workflow
python test_workflow.py
```

The test script will demonstrate:
- Importing transactions with automatic risk scoring
- Auto-reconciling low-risk transactions
- Posting accruals based on historical data
- Executing the autonomous month-end close process

## API Documentation

Once the service is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full Documentation**: Open `index.html` in your browser

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── schemas.py              # Pydantic models for request/response
│   ├── models/                 # SQLAlchemy database models
│   │   ├── database.py         # Database configuration
│   │   ├── transaction.py      # Transaction model
│   │   ├── accrual.py          # Accrual model
│   │   └── reconciliation.py   # Reconciliation record model
│   ├── services/               # Business logic layer
│   │   ├── transaction_service.py
│   │   ├── accrual_service.py
│   │   └── reconciliation_service.py
│   └── routers/                # API endpoints
│       ├── transactions.py
│       ├── accruals.py
│       └── reconciliation.py
├── index.html                  # Full documentation
├── requirements.txt            # Python dependencies
├── run_server.py              # Server startup script
└── test_workflow.py           # Workflow test script
```

## License

MIT License
