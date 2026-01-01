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

## API Endpoints

### Transactions

- `POST /transactions/import` - Import multiple transactions
- `GET /transactions` - List transactions with optional filtering

### Accruals

- `POST /accruals/payroll?period=2026-01` - Post payroll accrual for a period
- `POST /accruals/utilities?period=2026-01` - Post utilities accrual for a period
- `GET /accruals` - List accruals with optional filtering

### Reconciliation

- `POST /reconciliation/auto` - Auto-reconcile low-risk transactions
- `GET /reconciliation/status?period=2026-01` - Get reconciliation status
- `POST /reconciliation/month-end/close` - Perform autonomous month-end close

## Usage Examples

### 1. Import Transactions

```bash
curl -X POST "http://localhost:8000/transactions/import" \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {
        "description": "Employee salaries - January",
        "amount": 50000.00,
        "category": "payroll",
        "vendor": "Payroll Service Inc",
        "date": "2026-01-15T00:00:00"
      },
      {
        "description": "Office utilities",
        "amount": 1200.00,
        "category": "utilities",
        "vendor": "Power Company"
      }
    ]
  }'
```

### 2. Auto-Reconcile Low-Risk Transactions

```bash
curl -X POST "http://localhost:8000/reconciliation/auto" \
  -H "Content-Type: application/json" \
  -d '{
    "threshold": 50.0,
    "period": "2026-01"
  }'
```

### 3. Post Payroll Accrual

```bash
curl -X POST "http://localhost:8000/accruals/payroll?period=2026-01"
```

### 4. Post Utilities Accrual

```bash
curl -X POST "http://localhost:8000/accruals/utilities?period=2026-01"
```

### 5. Autonomous Month-End Close

```bash
curl -X POST "http://localhost:8000/reconciliation/month-end/close" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "2026-01",
    "auto_reconcile": true,
    "reconciliation_threshold": 50.0,
    "post_payroll_accrual": true,
    "post_utilities_accrual": true
  }'
```

### 6. Check Reconciliation Status

```bash
curl "http://localhost:8000/reconciliation/status?period=2026-01"
```

## Risk Scoring Model

The system uses a simplified risk scoring model (0-100) based on:

### Amount-Based Risk
- > $10,000: 50 points
- $5,000 - $10,000: 30 points
- $1,000 - $5,000: 15 points
- < $1,000: 5 points

### Category-Based Risk
- High-risk categories (consulting, legal, miscellaneous): +25 points
- Low-risk categories (utilities, payroll, rent, insurance): +5 points
- Other categories: +15 points

### Vendor-Based Risk
- Missing or empty vendor: +15 points

### Reconciliation Threshold
- Transactions with risk score ≤ threshold are auto-reconciled
- Default threshold: 50.0 (low-risk transactions only)

## Database Schema

### Transactions Table
- `id`: Primary key
- `date`: Transaction date
- `description`: Transaction description
- `amount`: Transaction amount
- `category`: Transaction category
- `vendor`: Vendor name
- `risk_score`: Calculated risk score (0-100)
- `is_reconciled`: Reconciliation status
- `reconciled_at`: Reconciliation timestamp

### Accruals Table
- `id`: Primary key
- `period`: Period (YYYY-MM)
- `accrual_type`: Type (payroll/utilities)
- `description`: Accrual description
- `amount`: Accrual amount
- `is_posted`: Posted status
- `based_on_historical`: Whether based on historical data
- `historical_average`: Historical average amount

### Reconciliation Records Table
- `id`: Primary key
- `period`: Period (YYYY-MM)
- `status`: Status (pending/in_progress/completed)
- `total_transactions`: Total transaction count
- `reconciled_count`: Reconciled transaction count
- `pending_count`: Pending transaction count
- `is_month_end_closed`: Month-end close status

## Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── schemas.py              # Pydantic models for request/response
├── models/                 # SQLAlchemy database models
│   ├── database.py         # Database configuration
│   ├── transaction.py      # Transaction model
│   ├── accrual.py          # Accrual model
│   └── reconciliation.py   # Reconciliation record model
├── services/               # Business logic layer
│   ├── transaction_service.py
│   ├── accrual_service.py
│   └── reconciliation_service.py
└── routers/                # API endpoints
    ├── transactions.py
    ├── accruals.py
    └── reconciliation.py
```

## Development

### Project Structure

The backend follows a clean architecture pattern:

1. **Models Layer**: SQLAlchemy ORM models for database entities
2. **Services Layer**: Business logic and domain operations
3. **Routers Layer**: FastAPI endpoints and request handling
4. **Schemas Layer**: Pydantic models for data validation

### Adding New Features

1. Define database models in `backend/models/`
2. Create service classes in `backend/services/`
3. Add API endpoints in `backend/routers/`
4. Register routers in `backend/main.py`

## License

MIT License
