"""Test workflow for Month-End Accounting Service.

This script demonstrates the complete workflow:
1. Import transactions with automatic risk scoring
2. Auto-reconcile low-risk transactions
3. Post accruals based on historical data
4. Execute the autonomous month-end close process
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(response):
    """Print formatted response."""
    if response.status_code >= 200 and response.status_code < 300:
        print(f"✓ Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"✗ Status: {response.status_code}")
        print(response.text)


def main():
    """Run the test workflow."""
    print_section("Month-End Accounting Service - Test Workflow")
    
    # Step 1: Import transactions
    print_section("Step 1: Import Transactions")
    transactions_data = {
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
                "amount": 800.00,
                "category": "utilities",
                "vendor": "Power Company"
            },
            {
                "description": "Office utilities - Water",
                "amount": 400.00,
                "category": "utilities",
                "vendor": "Water Services"
            },
            {
                "description": "Legal consultation",
                "amount": 5000.00,
                "category": "legal",
                "vendor": "Legal Associates"
            },
            {
                "description": "Office rent",
                "amount": 3000.00,
                "category": "rent",
                "vendor": "Property Management LLC"
            },
            {
                "description": "Miscellaneous expense",
                "amount": 15000.00,
                "category": "miscellaneous",
                "vendor": ""
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/transactions/import", json=transactions_data)
    print_response(response)
    
    # Step 2: View all transactions
    print_section("Step 2: List All Transactions")
    response = requests.get(f"{BASE_URL}/transactions")
    print_response(response)
    
    # Step 3: Auto-reconcile low-risk transactions
    print_section("Step 3: Auto-Reconcile Low-Risk Transactions (threshold=50)")
    reconcile_data = {
        "threshold": 50.0,
        "period": "2026-01"
    }
    response = requests.post(f"{BASE_URL}/reconciliation/auto", json=reconcile_data)
    print_response(response)
    
    # Step 4: Check reconciliation status
    print_section("Step 4: Check Reconciliation Status")
    response = requests.get(f"{BASE_URL}/reconciliation/status?period=2026-01")
    print_response(response)
    
    # Step 5: Post payroll accrual
    print_section("Step 5: Post Payroll Accrual")
    response = requests.post(f"{BASE_URL}/accruals/payroll?period=2026-01")
    print_response(response)
    
    # Step 6: Post utilities accrual
    print_section("Step 6: Post Utilities Accrual")
    response = requests.post(f"{BASE_URL}/accruals/utilities?period=2026-01")
    print_response(response)
    
    # Step 7: List all accruals
    print_section("Step 7: List All Accruals")
    response = requests.get(f"{BASE_URL}/accruals?period=2026-01")
    print_response(response)
    
    # Step 8: Perform month-end close
    print_section("Step 8: Autonomous Month-End Close")
    close_data = {
        "period": "2026-02",
        "auto_reconcile": True,
        "reconciliation_threshold": 50.0,
        "post_payroll_accrual": True,
        "post_utilities_accrual": True
    }
    response = requests.post(f"{BASE_URL}/reconciliation/month-end/close", json=close_data)
    print_response(response)
    
    # Step 9: Final status check
    print_section("Step 9: Final Reconciliation Status")
    response = requests.get(f"{BASE_URL}/reconciliation/status?period=2026-02")
    print_response(response)
    
    print_section("Workflow Complete!")
    print("\n✓ All steps executed successfully!")
    print("✓ Check the API documentation at http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the server.")
        print("✗ Please ensure the server is running: python run_server.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
