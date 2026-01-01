"""Simple script to run the FastAPI server."""

import uvicorn

if __name__ == "__main__":
    print("Starting Month-End Accounting Service...")
    print("API Documentation: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
