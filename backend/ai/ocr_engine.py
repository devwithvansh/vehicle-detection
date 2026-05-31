import re
from functools import lru_cache
from pathlib import Path

import cv2
import easyocr


PLATE_PATTERN = re.compile(
    r"[A-Z0-9]{5,20}"
)


@lru_cache
def get_reader():

    return easyocr.Reader(
        ["en"],
        gpu=False
    )


def clean_vehicle_number(
    text: str
):

    candidate = re.sub(
        r"[^A-Za-z0-9]",
        "",
        text.replace("↑", "")
    ).upper()

    matches = PLATE_PATTERN.findall(
        candidate
    )

    if not matches:
        return None

    return max(
        matches,
        key=len
    )


def single_pass(
    image
):

    results = get_reader().readtext(
        image,
        decoder="greedy",
        paragraph=False,
        detail=1,
        width_ths=0.7
    )

    best_text = None
    best_conf = 0.0

    for _, text, confidence in results:

        cleaned = clean_vehicle_number(
            text
        )

        if not cleaned:
            continue

        # Ignore side marking
        if cleaned == "210":
            continue

        # Ignore short garbage
        if len(cleaned) < 7:
            continue

        # Ignore pure numbers
        if cleaned.isdigit():
            continue

        if confidence > best_conf:

            best_text = cleaned
            best_conf = confidence

    return (
        best_text,
        best_conf
    )


def run_ocr(
    image_path: str | Path
):

    img = cv2.imread(
        str(image_path)
    )

    if img is None:
        return None, 0.0

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    attempts = [
        img,
        gray,
        thresh
    ]

    best_number = None
    best_confidence = 0.0

    for attempt in attempts:

        number, confidence = single_pass(
            attempt
        )

        if (
            number
            and confidence > best_confidence
        ):

            best_number = number
            best_confidence = confidence

    return (
        best_number,
        float(best_confidence)
    )