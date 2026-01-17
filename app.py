"""
Flask REST API for UK Tax Optimization

Provides RESTful endpoints for tax optimization calculations for:
- Company Directors
- Sole Traders
- Company Owners
- Landlords
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from backend.tax_optimization_engine import TaxOptimizationEngine
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize the optimization engine
optimizer = TaxOptimizationEngine()


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Tax Optimization API is running',
        'version': '1.0.0'
    }), 200


@app.route('/api/optimize/director', methods=['POST'])
def optimize_director():
    """
    Optimize tax position for a company director.
    
    Expected JSON body:
    {
        "salary": 30000.00,
        "dividends": 20000.00,
        "company_profit": 60000.00,
        "pension_contribution": 5000.00
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
        
        # Validate data types and ranges
        for field in ['salary', 'dividends', 'company_profit', 'pension_contribution']:
            if field in data:
                try:
                    value = float(data[field])
                    if value < 0:
                        return jsonify({
                            'error': f'{field} must be non-negative'
                        }), 400
                    data[field] = value
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'{field} must be a valid number'
                    }), 400
        
        # Set default for optional fields
        if 'pension_contribution' not in data:
            data['pension_contribution'] = 0
        
        # Perform optimization
        result = optimizer.optimize_director(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in optimize_director: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/optimize/sole-trader', methods=['POST'])
def optimize_sole_trader():
    """
    Optimize tax position for a sole trader.
    
    Expected JSON body:
    {
        "trading_income": 50000.00,
        "allowable_expenses": 8000.00,
        "pension_contribution": 3000.00,
        "capital_allowances": 2000.00
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['trading_income']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate data types and ranges
        for field in ['trading_income', 'allowable_expenses', 'pension_contribution', 'capital_allowances']:
            if field in data:
                try:
                    value = float(data[field])
                    if value < 0:
                        return jsonify({
                            'error': f'{field} must be non-negative'
                        }), 400
                    data[field] = value
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'{field} must be a valid number'
                    }), 400
        
        # Set defaults for optional fields
        if 'allowable_expenses' not in data:
            data['allowable_expenses'] = 0
        if 'pension_contribution' not in data:
            data['pension_contribution'] = 0
        if 'capital_allowances' not in data:
            data['capital_allowances'] = 0
        
        # Perform optimization
        result = optimizer.optimize_sole_trader(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in optimize_sole_trader: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/optimize/company-owner', methods=['POST'])
def optimize_company_owner():
    """
    Optimize tax position for a company owner.
    
    Expected JSON body:
    {
        "company_profit": 100000.00,
        "salary": 30000.00,
        "dividends": 40000.00,
        "r_and_d_expenditure": 15000.00,
        "capital_investment": 20000.00
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
        
        # Validate data types and ranges
        for field in ['company_profit', 'salary', 'dividends', 'r_and_d_expenditure', 'capital_investment']:
            if field in data:
                try:
                    value = float(data[field])
                    if value < 0:
                        return jsonify({
                            'error': f'{field} must be non-negative'
                        }), 400
                    data[field] = value
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'{field} must be a valid number'
                    }), 400
        
        # Set defaults for optional fields
        if 'r_and_d_expenditure' not in data:
            data['r_and_d_expenditure'] = 0
        if 'capital_investment' not in data:
            data['capital_investment'] = 0
        
        # Perform optimization
        result = optimizer.optimize_company_owner(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in optimize_company_owner: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/optimize/landlord', methods=['POST'])
def optimize_landlord():
    """
    Optimize tax position for a landlord.
    
    Expected JSON body:
    {
        "rental_income": 30000.00,
        "mortgage_interest": 8000.00,
        "other_expenses": 5000.00,
        "is_furnished": true,
        "number_of_properties": 2
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['rental_income']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate data types and ranges
        for field in ['rental_income', 'mortgage_interest', 'other_expenses']:
            if field in data:
                try:
                    value = float(data[field])
                    if value < 0:
                        return jsonify({
                            'error': f'{field} must be non-negative'
                        }), 400
                    data[field] = value
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'{field} must be a valid number'
                    }), 400
        
        # Validate boolean and integer fields
        if 'is_furnished' in data and not isinstance(data['is_furnished'], bool):
            return jsonify({
                'error': 'is_furnished must be a boolean'
            }), 400
        
        if 'number_of_properties' in data:
            try:
                value = int(data['number_of_properties'])
                if value < 1:
                    return jsonify({
                        'error': 'number_of_properties must be at least 1'
                    }), 400
                data['number_of_properties'] = value
            except (ValueError, TypeError):
                return jsonify({
                    'error': 'number_of_properties must be a valid integer'
                }), 400
        
        # Set defaults for optional fields
        if 'mortgage_interest' not in data:
            data['mortgage_interest'] = 0
        if 'other_expenses' not in data:
            data['other_expenses'] = 0
        if 'is_furnished' not in data:
            data['is_furnished'] = False
        if 'number_of_properties' not in data:
            data['number_of_properties'] = 1
        
        # Perform optimization
        result = optimizer.optimize_landlord(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in optimize_landlord: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


def print_routes():
    """Print available API routes."""
    print("\n" + "=" * 60)
    print("Starting Tax Optimization API...")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  - POST /api/optimize/director")
    print("  - POST /api/optimize/sole-trader")
    print("  - POST /api/optimize/company-owner")
    print("  - POST /api/optimize/landlord")
    print("  - GET  /api/health")
    print("\nServer running on: http://localhost:5000")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    print_routes()
    # Note: Debug mode should be disabled in production
    # Set debug=False or use a production WSGI server like Gunicorn
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
