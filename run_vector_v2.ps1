# VECTOR VXP2 PROTOTYPE 1.0-B - Windows Boot Protocol
# Launching Hybrid AI-Physics Mission Control Stack

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      INITIATING VECTOR VXP2 PROTOTYPE ARCHITECTURE       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$VENV_PATH = "$PSScriptRoot\.venv\Scripts"
$PYTHON_EXEC = "$VENV_PATH\python.exe"

# 1. Start the FastAPI Mission Control Microservice in a new background process
Write-Host "[1/2] Launching Fast-API Mission Control Microservice (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$VENV_PATH\uvicorn.exe' src.api_service:app --reload --port 8000" -WindowStyle Normal

# 2. Start the Streamlit Dashboard in a new background process
Write-Host "[2/2] Launching Streamlit Telemetry Dashboard (Port 8501)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$VENV_PATH\streamlit.exe' run src/app.py" -WindowStyle Normal

Write-Host ""
Write-Host "🚀 VECTOR VXP2 PROTOTYPE 1.0-B IS LIVE - System Status: NOMINAL" -ForegroundColor Green
Write-Host "----------------------------------------------------------"
Write-Host "► Dashboard: http://localhost:8501" -ForegroundColor Gray
Write-Host "► API Docs:  http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "----------------------------------------------------------"
