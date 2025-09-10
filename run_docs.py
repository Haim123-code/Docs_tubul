import subprocess
import time
import webview
import os
import sys
import shutil

# Use the current Python interpreter to launch uvicorn so it works on Windows too
BACKEND_CMD = [
    sys.executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "127.0.0.1",
    "--port",
    "8000",
]

# npm is executed differently on Windows (npm.cmd)
npm_exec = "npm.cmd" if os.name == "nt" else "npm"
FRONTEND_CMD = [npm_exec, "run", "dev"]


def start_process(cmd, cwd):
    """Start a subprocess after verifying the executable exists."""
    exe = cmd[0]
    if shutil.which(exe) is None and not os.path.isabs(exe):
        raise FileNotFoundError(f"Required command '{exe}' was not found. Is it installed?")
    return subprocess.Popen(cmd, cwd=cwd)


def main():
    base_dir = os.path.dirname(__file__)
    backend = start_process(BACKEND_CMD, os.path.join(base_dir, "backend"))
    frontend = start_process(FRONTEND_CMD, os.path.join(base_dir, "frontend"))
    time.sleep(3)
    try:
        webview.create_window("Collaborative Docs", "http://localhost:5173", width=1200, height=800)
        webview.start()
    finally:
        for proc in (backend, frontend):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
