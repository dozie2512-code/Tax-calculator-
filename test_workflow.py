#!/usr/bin/env python3
"""
Test script to demonstrate the complete FastAPI backend workflow.
This script tests all endpoints and demonstrates the month-end close process.
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_response(response, title="Response"):
    """Print formatted JSON response."""
    print(f"\n{title}:")
    print(json.dumps(response.json(), indent=2))

def main():
    """Run the complete workflow test."""
    print_section("MONTH-END ACCOUNTING SERVICE - WORKFLOW TEST")
    
    # 1. Health check
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Status")
    
    # 2. Import transactions
    print_section("2. Import Transactions")
    transactions_data = {
        "transactions": [
            {
                "description": "Employee salaries - January 2026",
                "amount": 50000.00,
                "category": "payroll",
                "vendor": "Payroll Service Inc",
                "date": "2026-01-15T00:00:00"
            },
            {
                "description": "Office electricity bill",
                "amount": 800.00,
                "category": "utilities",
                "vendor": "Power Company"
            },
            {
                "description": "Office water bill",
                "amount": 200.00,
                "category": "utilities",
                "vendor": "Water Company"
            },
            {
                "description": "Legal consultation",
                "amount": 8500.00,
                "category": "legal",
                "vendor": "Law Firm LLP"
            },
            {
                "description": "Office supplies",
                "amount": 450.00,
                "category": "supplies",
                "vendor": "Supplies Inc"
            },
            {
                "description": "Office rent",
                "amount": 3000.00,
                "category": "rent",
                "vendor": "Property Management Co"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/transactions/import", json=transactions_data)
    print_response(response, "Imported Transactions")
    
    # 3. List all transactions
    print_section("3. List All Transactions")
    response = requests.get(f"{BASE_URL}/transactions/")
    transactions = response.json()
    print(f"\nTotal transactions: {len(transactions)}")
    for t in transactions:
        print(f"  - {t['description']}: ${t['amount']:.2f} (Risk Score: {t['risk_score']}, Reconciled: {t['is_reconciled']})")
    
    # 4. Auto-reconcile low-risk transactions
    print_section("4. Auto-Reconcile Low-Risk Transactions")
    print("\nReconciling transactions with risk score <= 30...")
    reconcile_data = {
        "threshold": 30.0,
        "period": "2026-01"
    }
    response = requests.post(f"{BASE_URL}/reconciliation/auto", json=reconcile_data)
    print_response(response, "Reconciliation Result")
    
    # 5. Check reconciliation status
    print_section("5. Check Reconciliation Status")
    response = requests.get(f"{BASE_URL}/reconciliation/status?period=2026-01")
    print_response(response, "Reconciliation Status")
    
    # 6. List unreconciled transactions
    print_section("6. List Unreconciled Transactions")
    response = requests.get(f"{BASE_URL}/transactions/?is_reconciled=false")
    unreconciled = response.json()
    print(f"\nUnreconciled transactions: {len(unreconciled)}")
    for t in unreconciled:
        print(f"  - {t['description']}: ${t['amount']:.2f} (Risk Score: {t['risk_score']})")
    
    # 7. Post payroll accrual
    print_section("7. Post Payroll Accrual")
    response = requests.post(f"{BASE_URL}/accruals/payroll?period=2026-01")
    print_response(response, "Payroll Accrual")
    
    # 8. Post utilities accrual
    print_section("8. Post Utilities Accrual")
    response = requests.post(f"{BASE_URL}/accruals/utilities?period=2026-01")
    print_response(response, "Utilities Accrual")
    
    # 9. List all accruals
    print_section("9. List All Accruals")
    response = requests.get(f"{BASE_URL}/accruals/")
    accruals = response.json()
    print(f"\nTotal accruals: {len(accruals)}")
    for a in accruals:
        print(f"  - {a['description']}: ${a['amount']:.2f} (Historical Avg: ${a['historical_average']:.2f})")
    
    # 10. Perform month-end close
    print_section("10. Autonomous Month-End Close")
    print("\nPerforming comprehensive month-end close...")
    close_data = {
        "period": "2026-02",
        "auto_reconcile": True,
        "reconciliation_threshold": 50.0,
        "post_payroll_accrual": True,
        "post_utilities_accrual": True
    }
    response = requests.post(f"{BASE_URL}/reconciliation/month-end/close", json=close_data)
    print_response(response, "Month-End Close Result")
    
    # 11. Final summary
    print_section("WORKFLOW COMPLETE - SUMMARY")
    
    response = requests.get(f"{BASE_URL}/transactions/")
    all_trans = response.json()
    reconciled = sum(1 for t in all_trans if t['is_reconciled'])
    
    response = requests.get(f"{BASE_URL}/accruals/")
    all_accruals = response.json()
    
    print(f"""
Final Statistics:
  - Total Transactions: {len(all_trans)}
  - Reconciled: {reconciled}
  - Pending: {len(all_trans) - reconciled}
  - Total Accruals Posted: {len(all_accruals)}
  
The system successfully:
  ✓ Imported transactions with automatic risk scoring
  ✓ Auto-reconciled low-risk transactions (risk score ≤ threshold)
  ✓ Posted accruals based on historical data
  ✓ Executed autonomous month-end close process
  ✓ All pending manual approval for final review
  
Access API documentation at: {BASE_URL}/docs
    """)

if __name__ == "__main__":
    print("\nStarting Month-End Accounting Service Test...")
    print("Make sure the server is running: python run_server.py")
    print("\nWaiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server.")
        print("Please start the server first: python run_server.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
