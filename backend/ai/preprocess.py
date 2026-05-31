from pathlib import Path

import cv2
import numpy as np


def preprocess_plate_image(
    input_path: str | Path,
    output_path: str | Path
) -> str:

    image = cv2.imread(
        str(input_path)
    )

    if image is None:
        raise ValueError(
            "Unable to read image"
        )

    h, w = image.shape[:2]

    # Focus on bumper center region
    crop = image[
        int(h * 0.49):int(h * 0.67),
        int(w * 0.22):int(w * 0.62)
    ]

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.bilateralFilter(
        gray,
        5,
        50,
        50
    )

    gray = cv2.convertScaleAbs(
        gray,
        alpha=1.8,
        beta=25
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    debug_dir = (
        output_path.parent
        / "debug"
    )

    debug_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    cv2.imwrite(
        str(debug_dir / "crop.jpg"),
        crop
    )

    cv2.imwrite(
        str(debug_dir / "gray.jpg"),
        gray
    )

    resized = cv2.resize(
        gray,
        None,
        fx=5,
        fy=5,
        interpolation=cv2.INTER_CUBIC
    )

    _, thresh = cv2.threshold(
        resized,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    kernel = np.ones(
        (2, 2),
        np.uint8
    )

    processed = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    cv2.imwrite(
        str(debug_dir / "processed.jpg"),
        processed
    )

    cv2.imwrite(
        str(output_path),
        processed
    )

    return str(output_path)