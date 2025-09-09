import subprocess
import time
import webview
import os

BACKEND_CMD = ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
FRONTEND_CMD = ["npm", "run", "dev"]


def start_process(cmd, cwd):
    return subprocess.Popen(cmd, cwd=cwd)


def main():
    backend = start_process(BACKEND_CMD, os.path.join(os.path.dirname(__file__), "backend"))
    frontend = start_process(FRONTEND_CMD, os.path.join(os.path.dirname(__file__), "frontend"))
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
