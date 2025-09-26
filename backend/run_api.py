#!/usr/bin/env python3
"""
Smart Farm API Launcher
Simple launcher for the soil analysis API
"""

import sys
import os

# Add the soil_analysis directory to Python path
soil_analysis_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soil_analysis')
sys.path.insert(0, soil_analysis_path)

# Import and run the API
from api import app

if __name__ == '__main__':
    print("🚀 Starting Smart Farm API Server...")
    print("📍 Server will be available at: http://localhost:5001")
    print("🔍 Health check: http://localhost:5001/api/health")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")
