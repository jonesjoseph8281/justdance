#!/usr/bin/env python3
"""
Just Dance Clone - Startup Script
This script helps you start the backend server and provides instructions for the frontend.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        'flask',
        'flask_cors', 
        'cv2',
        'mediapipe',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'flask_cors':
                import flask_cors
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def start_backend():
    """Start the Flask backend server."""
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    print("🚀 Starting backend server...")
    print("   Server will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function."""
    print("🎵 Just Dance Clone 🎵")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\n📋 Setup Instructions:")
    print("1. Backend server will start automatically")
    print("2. Open frontend/index.html in your browser")
    print("3. Or serve frontend with: python -m http.server 8000")
    print("4. Upload a dance video and start dancing!")
    print("-" * 50)
    
    # Ask user if they want to start backend
    response = input("Start backend server now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        start_backend()
    else:
        print("💡 To start manually, run:")
        print("   cd backend && python app.py")

if __name__ == "__main__":
    main() 