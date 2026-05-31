from pathlib import Path


def test_required_project_structure_exists():
    root = Path(__file__).resolve().parents[1]
    for relative in [
        "backend/app/main.py",
        "backend/ai/preprocess.py",
        "backend/ai/ocr_engine.py",
        "backend/ai/detector.py",
        "frontend/src/App.jsx",
        "storage/captures",
        "storage/processed",
        "docs/API.md",
    ]:
        assert (root / relative).exists()
