"""
Enhanced FastAPI Backend for PDF-AGENT
BMAD Framework Implementation
"""

import os
import sys
import uuid
import json
import signal
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Pydantic Models
class RPATaskRequest(BaseModel):
    task_name: str
    parameters: Optional[Dict[str, Any]] = {}
    async_execution: bool = True

class WorkflowRequest(BaseModel):
    name: str
    description: str
    script_path: str
    parameters: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Workflow name cannot be empty')
        return v.strip()

class WorkflowUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    script_path: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

class StartWorkflowRequest(BaseModel):
    workflow_id: str
    script_path: str

class StopRequest(BaseModel):
    pid: int

class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: str
    script_path: str
    parameters: Dict[str, Any]
    tags: List[str]
    created_at: str
    updated_at: str
    status: str = "idle"

class TaskResponse(BaseModel):
    task_id: str
    task_name: str
    status: str
    message: str
    started_at: str
    log_file: Optional[str] = None

# FastAPI App
app = FastAPI(
    title="PDF-AGENT Enhanced API",
    description="Complete RPA Workflow Management System",
    version="2.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global Storage
running_processes: Dict[str, Dict] = {}
workflows_db: Dict[str, Dict] = {}
task_history: List[Dict] = []

# Utility Functions
def get_project_root() -> str:
    """Get the project root directory"""
    return os.path.dirname(os.path.abspath(__file__ + "/../"))

def get_python_exe() -> str:
    """Get the Python executable path, preferring virtual environment"""
    project_root = get_project_root()
    venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    
    if os.path.exists(venv_python):
        logger.info(f"Using virtual environment Python: {venv_python}")
        return venv_python
    
    python_exe = sys.executable or "python"
    logger.info(f"Using system Python: {python_exe}")
    return python_exe

def get_logs_dir() -> str:
    """Get logs directory path"""
    project_root = get_project_root()
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir

def get_scripts_dir() -> str:
    """Get scripts directory path"""
    project_root = get_project_root()
    scripts_dir = os.path.join(project_root, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    return scripts_dir

async def execute_rpa_script(script_path: str, task_id: str, parameters: Dict = None) -> Dict:
    """Execute RPA script asynchronously"""
    try:
        project_root = get_project_root()
        full_script_path = os.path.join(project_root, script_path)
        
        if not os.path.exists(full_script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Create log file
        logs_dir = get_logs_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"task_{task_id}_{timestamp}.log")
        
        # Prepare command
        python_exe = get_python_exe()
        cmd = [python_exe, full_script_path, "--non-interactive"]
        
        # Set environment
        env = os.environ.copy()
        env.update({
            'PYTHONIOENCODING': 'utf-8',
            'PYTHONUTF8': '1',
            'NON_INTERACTIVE': 'true'
        })
        
        # Execute script
        with open(log_file, 'w', encoding='utf-8', errors='replace') as log_fp:
            process = subprocess.Popen(
                cmd,
                cwd=project_root,
                stdout=log_fp,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            
            # Store process info
            running_processes[task_id] = {
                'pid': process.pid,
                'task_id': task_id,
                'script_path': script_path,
                'started_at': datetime.now().isoformat(),
                'log_file': log_file,
                'process': process
            }
            
            # Wait for completion (non-blocking)
            return_code = process.wait()
            
            # Update status
            if task_id in running_processes:
                running_processes[task_id]['completed_at'] = datetime.now().isoformat()
                running_processes[task_id]['return_code'] = return_code
                running_processes[task_id]['status'] = 'completed' if return_code == 0 else 'failed'
            
            return {
                'task_id': task_id,
                'pid': process.pid,
                'status': 'completed' if return_code == 0 else 'failed',
                'return_code': return_code,
                'log_file': log_file
            }
            
    except Exception as e:
        logger.error(f"Error executing script {script_path}: {e}")
        if task_id in running_processes:
            running_processes[task_id]['status'] = 'error'
            running_processes[task_id]['error'] = str(e)
        raise HTTPException(status_code=500, detail=f"Script execution failed: {str(e)}")

# API Routes

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "PDF-AGENT Enhanced API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    project_root = get_project_root()
    return {
        "status": "healthy",
        "project_root": project_root,
        "python_executable": get_python_exe(),
        "logs_directory": get_logs_dir(),
        "scripts_directory": get_scripts_dir(),
        "running_processes": len(running_processes),
        "total_workflows": len(workflows_db),
        "timestamp": datetime.now().isoformat()
    }

# RPA Task Endpoints
@app.post("/api/rpa/{task_name}", response_model=TaskResponse, tags=["RPA Tasks"])
async def execute_rpa_task(
    task_name: str, 
    request: RPATaskRequest, 
    background_tasks: BackgroundTasks
):
    """Execute RPA task by name"""
    try:
        # Map task names to script paths
        task_mapping = {
            "extract-data": "web_scraping_workflow.py",
            "process-pdf": "final_complete_workflow.py",
            "fill-and-send": "fill_and_send_workflow.py",
            "data-processing": "data_processing_workflow.py",
            "email-automation": "email_automation_workflow.py",
            "file-management": "file_management_workflow.py",
            "partial-workflow": "run_partial.py"
        }
        
        if task_name not in task_mapping:
            raise HTTPException(
                status_code=404, 
                detail=f"Task '{task_name}' not found. Available tasks: {list(task_mapping.keys())}"
            )
        
        script_path = task_mapping[task_name]
        task_id = str(uuid.uuid4())
        
        logger.info(f"Starting RPA task: {task_name} (ID: {task_id})")
        
        if request.async_execution:
            # Execute in background
            background_tasks.add_task(
                execute_rpa_script, 
                script_path, 
                task_id, 
                request.parameters
            )
            
            # Add to task history
            task_history.append({
                'task_id': task_id,
                'task_name': task_name,
                'script_path': script_path,
                'status': 'started',
                'started_at': datetime.now().isoformat(),
                'parameters': request.parameters
            })
            
            return TaskResponse(
                task_id=task_id,
                task_name=task_name,
                status="started",
                message=f"Task '{task_name}' started successfully",
                started_at=datetime.now().isoformat()
            )
        else:
            # Execute synchronously
            result = await execute_rpa_script(script_path, task_id, request.parameters)
            
            return TaskResponse(
                task_id=task_id,
                task_name=task_name,
                status=result['status'],
                message=f"Task '{task_name}' completed",
                started_at=datetime.now().isoformat(),
                log_file=result.get('log_file')
            )
            
    except Exception as e:
        logger.error(f"Error executing RPA task {task_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rpa/tasks", tags=["RPA Tasks"])
async def list_available_tasks():
    """List all available RPA tasks"""
    tasks = {
        "extract-data": {
            "name": "Data Extraction",
            "description": "Web scraping and data extraction workflow",
            "script": "web_scraping_workflow.py"
        },
        "process-pdf": {
            "name": "PDF Processing",
            "description": "Complete PDF processing workflow",
            "script": "final_complete_workflow.py"
        },
        "fill-and-send": {
            "name": "Fill and Send",
            "description": "PDF form filling and email workflow",
            "script": "fill_and_send_workflow.py"
        },
        "data-processing": {
            "name": "Data Processing",
            "description": "Data analysis and reporting workflow",
            "script": "data_processing_workflow.py"
        },
        "email-automation": {
            "name": "Email Automation",
            "description": "Bulk email operations workflow",
            "script": "email_automation_workflow.py"
        },
        "file-management": {
            "name": "File Management",
            "description": "File organization and cleanup workflow",
            "script": "file_management_workflow.py"
        },
        "partial-workflow": {
            "name": "Partial Workflow",
            "description": "Testing workflow for development",
            "script": "run_partial.py"
        }
    }
    
    return {
        "tasks": tasks,
        "total_count": len(tasks),
        "available_endpoints": [f"/api/rpa/{task}" for task in tasks.keys()]
    }

@app.get("/api/rpa/status/{task_id}", tags=["RPA Tasks"])
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    if task_id not in running_processes:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = running_processes[task_id]
    
    # Read logs if available
    logs = []
    if 'log_file' in task_info and os.path.exists(task_info['log_file']):
        try:
            with open(task_info['log_file'], 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.readlines()[-50:]  # Last 50 lines
        except Exception as e:
            logger.warning(f"Could not read log file: {e}")
    
    return {
        "task_id": task_id,
        "status": task_info.get('status', 'running'),
        "script_path": task_info['script_path'],
        "started_at": task_info['started_at'],
        "completed_at": task_info.get('completed_at'),
        "return_code": task_info.get('return_code'),
        "log_file": task_info.get('log_file'),
        "logs": logs,
        "error": task_info.get('error')
    }

# Workflow CRUD Endpoints
@app.post("/api/workflows", response_model=WorkflowResponse, tags=["Workflows"])
async def create_workflow(workflow: WorkflowRequest):
    """Create a new workflow"""
    try:
        workflow_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        workflow_data = {
            "id": workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "script_path": workflow.script_path,
            "parameters": workflow.parameters or {},
            "tags": workflow.tags or [],
            "created_at": timestamp,
            "updated_at": timestamp,
            "status": "idle"
        }
        
        workflows_db[workflow_id] = workflow_data
        
        logger.info(f"Created workflow: {workflow.name} (ID: {workflow_id})")
        
        return WorkflowResponse(**workflow_data)
        
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workflows", tags=["Workflows"])
async def list_workflows():
    """List all workflows"""
    workflows = list(workflows_db.values())
    return {
        "workflows": workflows,
        "total_count": len(workflows)
    }

@app.get("/api/workflows/{workflow_id}", response_model=WorkflowResponse, tags=["Workflows"])
async def get_workflow(workflow_id: str):
    """Get a specific workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return WorkflowResponse(**workflows_db[workflow_id])

@app.put("/api/workflows/{workflow_id}", response_model=WorkflowResponse, tags=["Workflows"])
async def update_workflow(workflow_id: str, update_data: WorkflowUpdateRequest):
    """Update a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    
    # Update fields if provided
    if update_data.name is not None:
        workflow["name"] = update_data.name
    if update_data.description is not None:
        workflow["description"] = update_data.description
    if update_data.script_path is not None:
        workflow["script_path"] = update_data.script_path
    if update_data.parameters is not None:
        workflow["parameters"] = update_data.parameters
    if update_data.tags is not None:
        workflow["tags"] = update_data.tags
    
    workflow["updated_at"] = datetime.now().isoformat()
    
    logger.info(f"Updated workflow: {workflow['name']} (ID: {workflow_id})")
    
    return WorkflowResponse(**workflow)

@app.delete("/api/workflows/{workflow_id}", tags=["Workflows"])
async def delete_workflow(workflow_id: str):
    """Delete a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_name = workflows_db[workflow_id]["name"]
    del workflows_db[workflow_id]
    
    logger.info(f"Deleted workflow: {workflow_name} (ID: {workflow_id})")
    
    return {"message": f"Workflow '{workflow_name}' deleted successfully"}

@app.post("/api/workflows/{workflow_id}/run", tags=["Workflows"])
async def run_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """Run a specific workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    task_id = str(uuid.uuid4())
    
    logger.info(f"Running workflow: {workflow['name']} (ID: {workflow_id})")
    
    # Execute workflow script
    background_tasks.add_task(
        execute_rpa_script,
        workflow['script_path'],
        task_id,
        workflow['parameters']
    )
    
    # Update workflow status
    workflow['status'] = 'running'
    workflow['last_run'] = datetime.now().isoformat()
    
    return {
        "message": f"Workflow '{workflow['name']}' started successfully",
        "task_id": task_id,
        "workflow_id": workflow_id,
        "started_at": datetime.now().isoformat()
    }

# Legacy endpoints for backward compatibility
@app.post("/workflows/start", tags=["Legacy"])
async def start_workflow_legacy(request: StartWorkflowRequest, background_tasks: BackgroundTasks):
    """Legacy endpoint for starting workflows"""
    task_id = str(uuid.uuid4())
    
    background_tasks.add_task(
        execute_rpa_script,
        request.script_path,
        task_id
    )
    
    return {
        "success": True,
        "proc_id": task_id,
        "pid": None,  # Will be set when process starts
        "log_file": f"logs/task_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    }

@app.get("/workflows", tags=["Legacy"])
async def list_running_workflows_legacy():
    """Legacy endpoint for listing running workflows"""
    running = []
    for task_id, process_info in running_processes.items():
        if process_info.get('status', 'running') == 'running':
            running.append({
                "pid": process_info['pid'],
                "workflow_id": task_id,
                "script_path": process_info['script_path'],
                "started_at": process_info['started_at'],
                "log_file": process_info['log_file']
            })
    
    return {"running": running}

@app.get("/workflows/status/{pid}", tags=["Legacy"])
async def get_workflow_status_legacy(pid: int):
    """Legacy endpoint for getting workflow status by PID"""
    # Find task by PID
    task_info = None
    for process_info in running_processes.values():
        if process_info['pid'] == pid:
            task_info = process_info
            break
    
    if not task_info:
        return {"running": False, "logs": ["Process not found"]}
    
    # Check if process is still running
    is_running = task_info.get('status', 'running') == 'running'
    
    # Read logs
    logs = []
    if 'log_file' in task_info and os.path.exists(task_info['log_file']):
        try:
            with open(task_info['log_file'], 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.readlines()
        except Exception as e:
            logs = [f"Error reading log file: {str(e)}"]
    
    return {
        "running": is_running,
        "logs": logs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
