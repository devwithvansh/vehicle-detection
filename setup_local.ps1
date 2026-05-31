# Setup script for Vehicle Detector (Local Installation - Windows)
# This script installs dependencies and prepares the environment without using a venv.

Write-Host "Starting local setup for Vehicle Detector..." -ForegroundColor Cyan

# 1. Install Backend Dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt
cd ..

# 2. Install Frontend Dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
cd frontend
npm install
cd ..

# 3. Prepare Storage Directories
Write-Host "Preparing storage directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "storage/captures"
New-Item -ItemType Directory -Force -Path "storage/processed"

# 4. Create .env files if they don't exist
if (-not (Test-Path "backend/.env")) {
    Write-Host "Creating backend/.env..." -ForegroundColor Yellow
    $secret = [Convert]::ToBase64String((1..32 | ForEach-Object { [byte](Get-Random -Minimum 0 -Maximum 256) }))
    $envContent = @"
SECRET_KEY=$secret
DATABASE_URL=mysql+pymysql://army_user:army_password@localhost:3306/army_vehicle_system
STORAGE_DIR=../storage
CORS_ORIGINS=http://localhost:5173
"@
    $envContent | Out-File -FilePath "backend/.env" -Encoding utf8
}

if (-not (Test-Path "frontend/.env")) {
    Write-Host "Creating frontend/.env..." -ForegroundColor Yellow
    "VITE_API_BASE_URL=http://localhost:8000/api" | Out-File -FilePath "frontend/.env" -Encoding utf8
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To run the project:"
Write-Host "1. Ensure MySQL is running and database 'army_vehicle_system' is created."
Write-Host "2. Start Backend: cd backend; uvicorn app.main:app --reload"
Write-Host "3. Start Frontend: cd frontend; npm run dev"
