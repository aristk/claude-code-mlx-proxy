#!/usr/bin/env python3
"""Stop the MLX proxy server running on port 8888"""
import subprocess
import sys
import time

def get_pid():
    """Get PID of process listening on port 8888"""
    try:
        result = subprocess.run(
            ["lsof", "-ti", ":8888"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip().split()[0])
    except Exception:
        pass
    return None

def main():
    pid = get_pid()

    if not pid:
        print("No server running on port 8888")
        return 0

    print(f"Stopping server (PID: {pid})...")

    # Try graceful shutdown first
    try:
        subprocess.run(["kill", str(pid)], check=True)
    except subprocess.CalledProcessError:
        print("Failed to send SIGTERM")
        return 1

    # Wait up to 3 seconds for graceful shutdown
    for _ in range(3):
        time.sleep(1)
        if not get_pid():
            print("Server stopped successfully")
            return 0

    # Force kill if still running
    print("Force stopping server...")
    try:
        subprocess.run(["kill", "-9", str(pid)], check=True)
        print("Server stopped")
        return 0
    except subprocess.CalledProcessError:
        print("Failed to stop server")
        return 1

if __name__ == "__main__":
    sys.exit(main())
