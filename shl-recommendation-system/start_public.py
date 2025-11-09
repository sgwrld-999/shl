#!/usr/bin/env python3
"""
Start server with public ngrok URL
Perfect for SHL submission testing
"""

import subprocess
import sys
import time
import os
import signal

# Configuration
PORT = int(os.getenv("PORT", 8000))
SERVER_FILE = "server.py"

print("=" * 70)
print("🌐 STARTING SERVER WITH PUBLIC URL")
print("=" * 70)
print()

# Check if ngrok is installed
print("📦 Checking dependencies...")
try:
    from pyngrok import ngrok
    print("   ✅ pyngrok installed")
except ImportError:
    print("   ⚠️  Installing pyngrok...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "pyngrok", "-q"
    ], check=True)
    from pyngrok import ngrok
    print("   ✅ pyngrok installed")

print()

# Start ngrok tunnel
print(f"🔗 Creating public tunnel to port {PORT}...")
try:
    public_url = ngrok.connect(PORT, bind_tls=True)
    
    print()
    print("=" * 70)
    print("✅ PUBLIC URL CREATED!")
    print("=" * 70)
    print()
    print(f"🌍 PUBLIC URL:")
    print(f"   {public_url}")
    print()
    print("📖 API DOCUMENTATION:")
    print(f"   {public_url}/docs")
    print()
    print("🧪 TEST ENDPOINTS:")
    print(f"   curl {public_url}/health")
    print()
    print(f"   curl -X POST {public_url}/recommend \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"query": "Need Java developer with 5 years experience"}\'')
    print()
    print("📋 FOR SHL SUBMISSION:")
    print(f"   API Base URL: {public_url}")
    print(f"   POST {public_url}/recommend")
    print(f"   GET  {public_url}/docs (interactive documentation)")
    print()
    print("=" * 70)
    print()
    print("🚀 Starting FastAPI server...")
    print("⏸️  Press Ctrl+C to stop both server and tunnel")
    print("=" * 70)
    print()
    
    # Start the server
    server_process = subprocess.Popen([
        sys.executable, SERVER_FILE
    ])
    
    try:
        # Keep running until Ctrl+C
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        server_process.terminate()
        server_process.wait()
        ngrok.kill()
        print("✅ Server and tunnel stopped")
        
except Exception as e:
    error_msg = str(e).lower()
    
    if "authentication failed" in error_msg or "authtoken" in error_msg:
        print(f"\n❌ Error: {e}")
        print()
        print("=" * 70)
        print("� NGROK AUTHENTICATION REQUIRED")
        print("=" * 70)
        print()
        print("🚀 FASTEST SOLUTION - Use Cloudflare Tunnel (no signup!):")
        print("   python start_cloudflare.py")
        print()
        print("   Cloudflare Tunnel is FREE and requires NO authentication!")
        print()
        print("=" * 70)
        print("OR - Set up ngrok (30 seconds):")
        print("=" * 70)
        print()
        print("1. Get your token:")
        print("   https://dashboard.ngrok.com/get-started/your-authtoken")
        print()
        print("2. Run this command:")
        print("   ngrok config add-authtoken YOUR_TOKEN_HERE")
        print()
        print("3. Restart this script:")
        print("   python start_public.py")
        print()
        print("=" * 70)
        print("OR - Run locally:")
        print("=" * 70)
        print()
        print(f"   python {SERVER_FILE}")
        print(f"   Access at: http://localhost:{PORT}/docs")
        print()
    else:
        print(f"\n❌ Error: {e}")
        print()
        print("💡 ALTERNATIVES:")
        print(f"   1. Use Cloudflare: python start_cloudflare.py")
        print(f"   2. Run locally: python {SERVER_FILE}")
    
    sys.exit(1)
