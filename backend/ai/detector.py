from pathlib import Path
from typing import Any

from app.core.config import get_settings


class YOLOVehicleDetector:
    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or get_settings().yolo_model_path
        self._model: Any | None = None

    def _load(self) -> Any | None:
        if not self.model_path:
            return None
        if self._model is None:
            from ultralytics import YOLO

            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image_path: str | Path) -> list[dict[str, Any]]:
        model = self._load()
        if model is None:
            return []
        detections = []
        for result in model(str(image_path)):
            for box in result.boxes:
                detections.append(
                    {
                        "class_id": int(box.cls[0]),
                        "confidence": float(box.conf[0]),
                        "xyxy": [float(value) for value in box.xyxy[0]],
                    }
                )
        return detections
