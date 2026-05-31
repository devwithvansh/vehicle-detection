# Army Vehicle Detector

A professional vehicle number plate recognition and registration system designed for military checkpoints.

## Key Features
- **Live OCR Scanning**: Capture vehicle plates via camera or upload.
- **Automatic Logging**: Registered vehicles are automatically logged with entry/exit times.
- **Instant Registration**: Unregistered vehicles trigger a redirect to a registration page with the detected number pre-filled.
- **MySQL Backend**: Robust data storage for vehicles and movement logs.
- **Modern Dashboard**: Real-time statistics and movement history.

## Local Setup (No Virtual Environment)

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL Server

### 1. Database Configuration
Create a MySQL database named `army_vehicle_system`:
```sql
CREATE DATABASE army_vehicle_system;
```

### 2. Installation
Run the setup script for your operating system:
- **Windows**: Right-click `setup_local.ps1` and select "Run with PowerShell".
- **Linux/Mac**: Run `bash setup_local.sh`.

Alternatively, install manually:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Running the Project
You will need two terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Default Credentials
- **Username**: `admin`
- **Password**: `Admin@12345`

## Project Structure
- `backend/`: FastAPI application and OCR engine.
- `frontend/`: React + Vite + Tailwind CSS dashboard.
- `storage/`: Local storage for captured and processed images.
- `docs/`: API documentation.
