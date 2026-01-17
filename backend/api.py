"""
Flask API for Tax Optimization Service

Provides RESTful endpoints for tax optimization recommendations
for different user types.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.tax_optimization_engine import TaxOptimizationEngine
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize optimization engine
optimizer = TaxOptimizationEngine()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Tax Optimization API is running'
    }), 200


@app.route('/api/optimize/director', methods=['POST'])
def optimize_director():
    """
    Optimize tax position for company directors.
    
    Expected JSON body:
    {
        "salary": float,
        "dividends": float,
        "company_profit": float,
        "pension_contribution": float (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['salary', 'dividends', 'company_profit']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        salary = float(data['salary'])
        dividends = float(data['dividends'])
        company_profit = float(data['company_profit'])
        pension_contribution = float(data.get('pension_contribution', 0))
        
        # Optimize
        result = optimizer.optimize_for_director(
            salary=salary,
            dividends=dividends,
            company_profit=company_profit,
            pension_contribution=pension_contribution
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/optimize/sole-trader', methods=['POST'])
def optimize_sole_trader():
    """
    Optimize tax position for sole traders.
    
    Expected JSON body:
    {
        "trading_income": float,
        "allowable_expenses": float,
        "pension_contribution": float (optional),
        "capital_allowances": float (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['trading_income', 'allowable_expenses']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        trading_income = float(data['trading_income'])
        allowable_expenses = float(data['allowable_expenses'])
        pension_contribution = float(data.get('pension_contribution', 0))
        capital_allowances = float(data.get('capital_allowances', 0))
        
        # Optimize
        result = optimizer.optimize_for_sole_trader(
            trading_income=trading_income,
            allowable_expenses=allowable_expenses,
            pension_contribution=pension_contribution,
            capital_allowances=capital_allowances
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/optimize/company-owner', methods=['POST'])
def optimize_company_owner():
    """
    Optimize tax position for company owners.
    
    Expected JSON body:
    {
        "company_profit": float,
        "salary": float,
        "dividends": float,
        "r_and_d_expenditure": float (optional),
        "capital_investment": float (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_profit', 'salary', 'dividends']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        company_profit = float(data['company_profit'])
        salary = float(data['salary'])
        dividends = float(data['dividends'])
        r_and_d_expenditure = float(data.get('r_and_d_expenditure', 0))
        capital_investment = float(data.get('capital_investment', 0))
        
        # Optimize
        result = optimizer.optimize_for_company_owner(
            company_profit=company_profit,
            salary=salary,
            dividends=dividends,
            r_and_d_expenditure=r_and_d_expenditure,
            capital_investment=capital_investment
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/optimize/landlord', methods=['POST'])
def optimize_landlord():
    """
    Optimize tax position for landlords.
    
    Expected JSON body:
    {
        "rental_income": float,
        "mortgage_interest": float,
        "other_expenses": float,
        "is_furnished": bool (optional),
        "number_of_properties": int (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['rental_income', 'mortgage_interest', 'other_expenses']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        rental_income = float(data['rental_income'])
        mortgage_interest = float(data['mortgage_interest'])
        other_expenses = float(data['other_expenses'])
        is_furnished = data.get('is_furnished', False)
        number_of_properties = int(data.get('number_of_properties', 1))
        
        # Optimize
        result = optimizer.optimize_for_landlord(
            rental_income=rental_income,
            mortgage_interest=mortgage_interest,
            other_expenses=other_expenses,
            is_furnished=is_furnished,
            number_of_properties=number_of_properties
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed'
    }), 405


if __name__ == '__main__':
    print("Starting Tax Optimization API...")
    print("Available endpoints:")
    print("  - POST /api/optimize/director")
    print("  - POST /api/optimize/sole-trader")
    print("  - POST /api/optimize/company-owner")
    print("  - POST /api/optimize/landlord")
    print("  - GET  /api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
