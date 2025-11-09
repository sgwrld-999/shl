#!/usr/bin/env python3
"""
Start server with Cloudflare Tunnel (FREE, no signup required)
Better than ngrok - no authentication needed!
"""

import subprocess
import sys
import time
import os
import signal
import re

PORT = 8000

print("=" * 80)
print("🌐 STARTING SERVER WITH CLOUDFLARE TUNNEL")
print("=" * 80)
print()

# Check if cloudflared is installed
def check_cloudflared():
    try:
        subprocess.run(["cloudflared", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Check for local cloudflared binary first
local_cloudflared = "./cloudflared"
if os.path.exists(local_cloudflared):
    CLOUDFLARED_CMD = local_cloudflared
    print("✅ Using local cloudflared binary")
elif check_cloudflared():
    CLOUDFLARED_CMD = "cloudflared"
    print("✅ Using system cloudflared")
else:
    print("❌ cloudflared not found!")
    print()
    print("=" * 80)
    print("📦 INSTALL CLOUDFLARED:")
    print("=" * 80)
    print()
    print("Option 1 - Via Homebrew (recommended):")
    print("   brew install cloudflared")
    print()
    print("Option 2 - Download directly:")
    print("   https://github.com/cloudflare/cloudflared/releases")
    print()
    print("Option 3 - Quick install script:")
    print('   curl -L "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz" | tar -xz')
    print("   chmod +x cloudflared")
    print()
    print("=" * 80)
    print()
    print("💡 OR use ngrok instead:")
    print("   python start_public.py")
    print()
    sys.exit(1)

print()

# Check if server is already running
def is_server_running():
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', PORT))
        sock.close()
        return result == 0
    except:
        return False

server_process = None
if is_server_running():
    print(f"✅ Server already running on port {PORT}")
else:
    print(f"🚀 Starting FastAPI server on port {PORT}")
    # Start the server in background
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start (non-blocking check)
    print("⏳ Waiting for server to initialize...", end="", flush=True)
    max_retries = 20
    for i in range(max_retries):
        if is_server_running():
            print(" Ready!")
            break
        print(".", end="", flush=True)
        time.sleep(0.5)
    else:
        print(" Timeout!")
        print("⚠️  Server may not be ready, but continuing anyway...")

print()
print("🔗 Creating Cloudflare tunnel...")
print("   (This may take 10-15 seconds...)")
print()

# Start cloudflared tunnel
try:
    cloudflared_cmd = CLOUDFLARED_CMD if 'CLOUDFLARED_CMD' in globals() else "cloudflared"
    tunnel_process = subprocess.Popen(
        [cloudflared_cmd, "tunnel", "--url", f"http://localhost:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Read and find the public URL
    public_url = None
    for line in tunnel_process.stdout:
        print(f"   {line.strip()}")
        
        # Look for the URL in various formats
        if "https://" in line and "trycloudflare.com" in line:
            # Try to extract URL using regex
            url_match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
            if url_match:
                public_url = url_match.group(1)
        
        if public_url:
            print()
            print("=" * 80)
            print("✅ PUBLIC URL CREATED!")
            print("=" * 80)
            print()
            print(f"🌍 PUBLIC URL:")
            print(f"   {public_url}")
            print()
            print("📖 API DOCUMENTATION:")
            print(f"   {public_url}/docs")
            print(f"   {public_url}/redoc")
            print()
            print("🧪 TEST ENDPOINTS:")
            print(f"   curl {public_url}/health")
            print()
            print("📨 GET RECOMMENDATIONS:")
            print(f"   curl -X POST {public_url}/recommend \\")
            print('     -H "Content-Type: application/json" \\')
            print('     -d \'{"query": "Need Java developer with 5 years experience", "max_results": 5}\'')
            print()
            print("=" * 80)
            print("💡 FOR SHL SUBMISSION:")
            print("=" * 80)
            print(f"   API Base URL: {public_url}")
            print(f"   Main Endpoint: POST {public_url}/recommend")
            print(f"   Documentation: {public_url}/docs")
            print()
            print("=" * 80)
            print("⏸️  Server is running. Press Ctrl+C to stop")
            print("=" * 80)
            print()
            break
    
    # Keep running and showing logs
    try:
        for line in tunnel_process.stdout:
            # Show important messages only
            if "error" in line.lower() or "warn" in line.lower():
                print(f"   {line.strip()}")
    except KeyboardInterrupt:
        pass
        
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    print("\n\n🛑 Stopping...")
    try:
        if 'tunnel_process' in locals():
            tunnel_process.terminate()
            tunnel_process.wait(timeout=5)
        if server_process:
            server_process.terminate()
            server_process.wait(timeout=5)
    except:
        if 'tunnel_process' in locals():
            try:
                tunnel_process.kill()
            except:
                pass
        if server_process:
            try:
                server_process.kill()
            except:
                pass
    print("✅ Stopped")
