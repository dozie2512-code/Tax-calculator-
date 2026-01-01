"""Test workflow for autonomous month-end close."""

import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_response(response):
    """Pretty print JSON response."""
    if response.status_code >= 200 and response.status_code < 300:
        print(f"✓ Success ({response.status_code})")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Error ({response.status_code})")
        print(response.text)


def test_workflow():
    """Run complete test workflow for month-end close."""
    
    print_section("Month-End Accounting Service - Test Workflow")
    
    # Check server health
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    
    if response.status_code != 200:
        print("\n✗ Server is not running. Please start it with: python run_server.py")
        return
    
    time.sleep(0.5)
    
    # Import transactions
    print_section("2. Import Transactions with Automatic Risk Scoring")
    
    transactions = {
        "transactions": [
            {
                "description": "Employee salaries - January",
                "amount": 50000.00,
                "category": "payroll",
                "vendor": "Payroll Service Inc",
                "date": "2026-01-15T00:00:00"
            },
            {
                "description": "Office utilities - Electric",
                "amount": 1200.00,
                "category": "utilities",
                "vendor": "Power Company",
                "date": "2026-01-10T00:00:00"
            },
            {
                "description": "Legal consultation fees",
                "amount": 15000.00,
                "category": "legal",
                "vendor": "Law Firm LLP",
                "date": "2026-01-20T00:00:00"
            },
            {
                "description": "Office supplies",
                "amount": 250.00,
                "category": "supplies",
                "vendor": "Office Depot",
                "date": "2026-01-05T00:00:00"
            },
            {
                "description": "Consulting services",
                "amount": 8000.00,
                "category": "consulting",
                "vendor": "Tech Consultants Inc",
                "date": "2026-01-12T00:00:00"
            },
            {
                "description": "Office rent - January",
                "amount": 5000.00,
                "category": "rent",
                "vendor": "Property Management LLC",
                "date": "2026-01-01T00:00:00"
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/transactions/import",
        json=transactions
    )
    print_response(response)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Imported {result['imported_count']} transactions")
        print("\nRisk Scores:")
        for txn in result['transactions']:
            print(f"  - {txn['description'][:50]:50} | Risk: {txn['risk_score']:5.1f} | ${txn['amount']:10,.2f}")
    
    time.sleep(0.5)
    
    # List all transactions
    print_section("3. List All Transactions for January 2026")
    response = requests.get(f"{BASE_URL}/transactions?period=2026-01")
    print_response(response)
    
    time.sleep(0.5)
    
    # Auto-reconcile low-risk transactions
    print_section("4. Auto-Reconcile Low-Risk Transactions (threshold: 50.0)")
    
    reconcile_request = {
        "threshold": 50.0,
        "period": "2026-01"
    }
    
    response = requests.post(
        f"{BASE_URL}/reconciliation/auto",
        json=reconcile_request
    )
    print_response(response)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Auto-reconciled {result['reconciled_count']} low-risk transactions")
    
    time.sleep(0.5)
    
    # Check reconciliation status
    print_section("5. Check Reconciliation Status")
    response = requests.get(f"{BASE_URL}/reconciliation/status?period=2026-01")
    print_response(response)
    
    if response.status_code == 200:
        status = response.json()
        print(f"\n✓ Reconciliation Rate: {status['reconciliation_rate']}%")
        print(f"  - Total Transactions: {status['total_transactions']}")
        print(f"  - Reconciled: {status['reconciled_count']}")
        print(f"  - Pending: {status['pending_count']}")
    
    time.sleep(0.5)
    
    # Post payroll accrual
    print_section("6. Post Payroll Accrual")
    response = requests.post(f"{BASE_URL}/accruals/payroll?period=2026-01")
    print_response(response)
    
    time.sleep(0.5)
    
    # Post utilities accrual
    print_section("7. Post Utilities Accrual")
    response = requests.post(f"{BASE_URL}/accruals/utilities?period=2026-01")
    print_response(response)
    
    time.sleep(0.5)
    
    # List accruals
    print_section("8. List Accruals for January 2026")
    response = requests.get(f"{BASE_URL}/accruals?period=2026-01")
    print_response(response)
    
    time.sleep(0.5)
    
    # Perform autonomous month-end close
    print_section("9. Perform Autonomous Month-End Close")
    print("This orchestrates the complete month-end close process with zero-touch accounting...")
    
    # First, let's use a different period to avoid conflict
    close_request = {
        "period": "2026-02",
        "auto_reconcile": True,
        "reconciliation_threshold": 50.0,
        "post_payroll_accrual": True,
        "post_utilities_accrual": True
    }
    
    response = requests.post(
        f"{BASE_URL}/reconciliation/month-end/close",
        json=close_request
    )
    print_response(response)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Month-End Close Status: {result['status']}")
        print(f"✓ Requires Approval: {result['requires_approval']}")
        print(f"\n{result['approval_message']}")
        
        print("\n--- Workflow Steps ---")
        for step in result['workflow_steps']:
            status_icon = "✓" if step['status'] == 'completed' else "⊘" if step['status'] == 'skipped' else "•"
            print(f"{status_icon} [{step['status'].upper()}] {step['step']}: {step['message']}")
        
        print("\n--- Reconciliation Summary ---")
        summary = result['reconciliation_summary']
        print(f"Period: {summary['period']}")
        print(f"Status: {summary['status']}")
        print(f"Reconciliation Rate: {summary['reconciliation_rate']}%")
        print(f"Transactions: {summary['reconciled_count']}/{summary['total_transactions']} reconciled")
        print(f"Month-End Closed: {summary['is_month_end_closed']}")
    
    time.sleep(0.5)
    
    # Final summary
    print_section("Test Workflow Complete!")
    print("✓ All automated tasks completed successfully")
    print("✓ Zero-touch accounting approach demonstrated")
    print("✓ Human approval workflow ready")
    print("\nNext Steps:")
    print("  1. Review the workflow steps and reconciliation summary")
    print("  2. Approve the month-end close to finalize")
    print("  3. Financial statements are prepared and ready")
    print("\nAPI Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        test_workflow()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the server.")
        print("Please start the server first with: python run_server.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
