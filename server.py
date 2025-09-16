import os
import sys
import uuid
import json
import signal
import subprocess
from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class StartRequest(BaseModel):
    workflow_id: str
    script_path: str


class StopRequest(BaseModel):
    pid: int


app = FastAPI(title="PDF-AGENT Workflow API")

# Allow local dev origins by default
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"  # Allow all origins for development
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # Set to False when using wildcard
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class ProcInfo(BaseModel):
    pid: int
    workflow_id: str
    script_path: str
    started_at: str
    log_file: str


processes: Dict[str, ProcInfo] = {}


def _workspace_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def _python_exe() -> str:
    # Try to use virtual environment Python first
    venv_python = os.path.join(_workspace_dir(), ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        print(f"[DEBUG] Using virtual environment Python: {venv_python}")
        return venv_python
    
    # Fallback to system Python
    python_exe = sys.executable or "python"
    print(f"[DEBUG] Using system Python: {python_exe}")
    return python_exe


def _logs_dir() -> str:
    path = os.path.join(_workspace_dir(), "logs")
    os.makedirs(path, exist_ok=True)
    return path


@app.get("/workflows")
def list_workflows():
    return {"running": list(processes.values())}


@app.post("/workflows/start")
def start_workflow(req: StartRequest):
    print(f"[DEBUG] Starting workflow: {req.workflow_id}, script: {req.script_path}")
    
    script_abs = os.path.join(_workspace_dir(), req.script_path)
    print(f"[DEBUG] Script absolute path: {script_abs}")
    
    if not os.path.exists(script_abs):
        print(f"[ERROR] Script not found: {script_abs}")
        raise HTTPException(status_code=404, detail=f"Script not found: {req.script_path}")

    log_path = os.path.join(
        _logs_dir(), f"workflow_{req.workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    print(f"[DEBUG] Log file: {log_path}")
    
    log_fp = open(log_path, "w", encoding="utf-8", errors="replace")

    # Launch subprocess non-blocking, capture stdout/stderr to log file
    try:
        python_cmd = [_python_exe(), script_abs]
        print(f"[DEBUG] Running command: {python_cmd}")
        print(f"[DEBUG] Working directory: {_workspace_dir()}")
        
        # Set environment variables for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        env['NON_INTERACTIVE'] = 'true'  # Enable non-interactive mode
        
        # Add non-interactive flag for scripts that support it
        if req.script_path in ['final_complete_workflow.py', 'fill_and_send_workflow.py', 'web_scraping_workflow.py', 'data_processing_workflow.py', 'email_automation_workflow.py', 'file_management_workflow.py']:
            python_cmd.append('--non-interactive')
        
        proc = subprocess.Popen(
            python_cmd,
            cwd=_workspace_dir(),
            stdout=log_fp,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
        print(f"[DEBUG] Process started with PID: {proc.pid}")
    except Exception as e:
        log_fp.close()
        print(f"[ERROR] Failed to start process: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start process: {e}")

    proc_id = str(uuid.uuid4())
    processes[proc_id] = ProcInfo(
        pid=proc.pid,
        workflow_id=req.workflow_id,
        script_path=req.script_path,
        started_at=datetime.now().isoformat(),
        log_file=log_path,
    )
    
    print(f"[DEBUG] Process registered with ID: {proc_id}")
    return {"success": True, "proc_id": proc_id, "pid": proc.pid, "log_file": log_path}


@app.post("/workflows/stop")
def stop_workflow(req: StopRequest):
    # Find proc by pid
    target_key: Optional[str] = None
    for key, info in processes.items():
        if info.pid == req.pid:
            target_key = key
            break

    if target_key is None:
        raise HTTPException(status_code=404, detail=f"PID not tracked: {req.pid}")

    try:
        if os.name == "nt":
            # Send CTRL-BREAK like signal to the process group; fallback to taskkill
            try:
                subprocess.run(["taskkill", "/PID", str(req.pid), "/T", "/F"], check=True)
            except subprocess.CalledProcessError:
                pass
        else:
            os.kill(req.pid, signal.SIGTERM)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop process: {e}")

    info = processes.pop(target_key)
    return {"success": True, "stopped": info}


@app.get("/workflows/status/{pid}")
def workflow_status(pid: int):
    # Determine if pid is alive
    alive = False
    try:
        if os.name == "nt":
            # tasklist check
            out = subprocess.check_output(["tasklist", "/FI", f"PID eq {pid}"], text=True)
            alive = str(pid) in out
        else:
            os.kill(pid, 0)
            alive = True
    except Exception:
        alive = False

    # Read last N lines from log, if exists
    log_lines = []
    log_file = None
    for info in processes.values():
        if info.pid == pid:
            log_file = info.log_file
            break
    if log_file and os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                log_lines = lines[-200:]
        except Exception:
            log_lines = []

    return {"running": alive, "logs": log_lines}


# Convenience root
@app.get("/")
def root():
    return {"service": "PDF-AGENT Workflow API", "running": True}


# To run:  uvicorn server:app --host 127.0.0.1 --port 8000 --reload

