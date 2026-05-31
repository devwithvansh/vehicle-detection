$ErrorActionPreference = "Stop"

Write-Host "Creating backend virtual environment..."
python -m venv backend\.venv
backend\.venv\Scripts\python -m pip install --upgrade pip
backend\.venv\Scripts\pip install -r backend\requirements.txt

if (-not (Test-Path backend\.env)) {
  Copy-Item backend\.env.example backend\.env
  Write-Host "Created backend\.env. Update DATABASE_URL with your MySQL password."
}

if (-not (Test-Path frontend\.env)) {
  Copy-Item frontend\.env.example frontend\.env
}

Write-Host "Installing frontend dependencies..."
Push-Location frontend
npm.cmd install
Pop-Location

Write-Host "Setup complete."
