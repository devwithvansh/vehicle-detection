#!/bin/bash

# Setup script for Vehicle Detector (Local Installation)
# This script installs dependencies and prepares the environment without using a venv.

set -e

echo "Starting local setup for Vehicle Detector..."

# 1. Install Backend Dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# 2. Install Frontend Dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# 3. Prepare Storage Directories
echo "Preparing storage directories..."
mkdir -p storage/captures
mkdir -p storage/processed

# 4. Create .env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env..."
    cat <<EOF > backend/.env
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=mysql+pymysql://army_user:army_password@localhost:3306/army_vehicle_system
STORAGE_DIR=../storage
CORS_ORIGINS=http://localhost:5173
EOF
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env..."
    echo "VITE_API_BASE_URL=http://localhost:8000/api" > frontend/.env
fi

echo "Setup complete!"
echo ""
echo "To run the project:"
echo "1. Ensure MySQL is running and database 'army_vehicle_system' is created."
echo "2. Start Backend: cd backend && uvicorn app.main:app --reload"
echo "3. Start Frontend: cd frontend && npm run dev"
