
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import os
import signal
import sys
import json

app = FastAPI()

# Configuration
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_PATH, "main.py")
CONFIG_FILE = os.path.join(SCRIPT_PATH, "config", "config.ini")
URL_CONFIG_FILE = os.path.join(SCRIPT_PATH, "config", "URL_config.ini")
STATUS_FILE = os.path.join(SCRIPT_PATH, "config", "web_status.json")
LOG_FILE = os.path.join(SCRIPT_PATH, "logs", "web_run.log")

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_PATH, "templates"), exist_ok=True)

# Templates
templates = Jinja2Templates(directory="templates")

# Global Process Handle
recorder_process = None

def is_process_running():
    global recorder_process
    if recorder_process is None:
        return False
    if recorder_process.poll() is None:
        return True
    return False

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def get_status():
    running = is_process_running()
    status = {}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                status = json.load(f)
        except:
            pass
    
    # Get recent logs
    logs = ""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                # Read last 5000 chars
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - 5000))
                logs = f.read()
        except:
            logs = "Error reading logs"

    return {
        "running": running,
        "status": status,
        "logs": logs
    }

@app.post("/api/start")
async def start_recorder():
    global recorder_process
    if is_process_running():
        return {"status": "error", "message": "Already running"}
    
    try:
        # Clear old log
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("--- Starting Recorder ---\n")

        python_exe = sys.executable
        log_f = open(LOG_FILE, 'a', encoding='utf-8')
        
        # Use Popen with unbuffered output (-u)
        recorder_process = subprocess.Popen(
            [python_exe, "-u", MAIN_SCRIPT],
            cwd=SCRIPT_PATH,
            stdout=log_f,
            stderr=subprocess.STDOUT
        )
        return {"status": "success", "message": "Started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/stop")
async def stop_recorder():
    global recorder_process
    if not is_process_running():
        return {"status": "error", "message": "Not running"}
    
    try:
        recorder_process.terminate()
        # Wait a bit
        try:
            recorder_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            recorder_process.kill()
            
        recorder_process = None
        return {"status": "success", "message": "Stopped"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/config")
async def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8-sig') as f:
            return {"content": f.read()}
    return {"content": ""}

@app.post("/api/config")
async def save_config(request: Request):
    data = await request.json()
    content = data.get("content")
    if content is not None:
        with open(CONFIG_FILE, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        return {"status": "success"}
    return {"status": "error"}

@app.get("/api/url_config")
async def get_url_config():
    if os.path.exists(URL_CONFIG_FILE):
        with open(URL_CONFIG_FILE, 'r', encoding='utf-8-sig') as f:
            return {"content": f.read()}
    return {"content": ""}

@app.post("/api/url_config")
async def save_url_config(request: Request):
    data = await request.json()
    content = data.get("content")
    if content is not None:
        with open(URL_CONFIG_FILE, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        return {"status": "success"}
    return {"status": "error"}

if __name__ == "__main__":
    print("Starting Web Interface on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
