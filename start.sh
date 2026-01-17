#!/bin/bash

# Tax Optimization Calculator - Startup Script

echo "======================================"
echo "Tax Optimization Calculator"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✓ pip is installed"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Start the Flask API
echo "Starting Flask API server..."
echo "API will be available at: http://localhost:5000"
echo ""
echo "Available endpoints:"
echo "  - POST /api/optimize/director"
echo "  - POST /api/optimize/sole-trader"
echo "  - POST /api/optimize/company-owner"
echo "  - POST /api/optimize/landlord"
echo "  - GET  /api/health"
echo ""
echo "To access the frontend, open frontend/tax_optimizer.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Run the API
python3 backend/api.py
