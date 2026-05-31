# API Overview

FastAPI exposes Swagger UI at `http://localhost:8000/docs`.

Core route groups:

- `POST /api/auth/login` for JWT login.
- `GET /api/dashboard/summary` for stats, chart data, and recent activity.
- `POST /api/ocr/capture` for image upload, OpenCV preprocessing, EasyOCR extraction, and automatic entry or exit logging.
- `GET/POST/PATCH /api/vehicles` for registry operations.
- `GET/POST /api/logs` plus `GET /api/logs/export.csv` for audit exports.
- `GET/POST /api/cameras` for multi-camera ready checkpoint locations.
