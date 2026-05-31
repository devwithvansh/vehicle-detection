import re
from functools import lru_cache
from pathlib import Path
import cv2
import easyocr

# Indian Army Plate Format: 
# [Arrow] [Year: 2 digits] [Class: 1 letter] [Serial: 5-7 digits] [Check: 1 letter]
# Example: ↑ 64 B 087985 E
ARMY_PLATE_PATTERN = re.compile(r"(?:[↑\^1T]\s*)?(\d{2})\s*([A-Z0-9])\s*(\d{5,7})\s*([A-Z0-9])")

@lru_cache
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

def force_letter(char: str) -> str:
    """Corrects common OCR digit-to-letter misinterpretations."""
    corrections = {
        '8': 'B',
        '0': 'D',
        '1': 'I',
        '5': 'S',
        '2': 'Z',
        '4': 'A'
    }
    return corrections.get(char, char.upper())

def force_digit(char: str) -> str:
    """Corrects common OCR letter-to-digit misinterpretations."""
    corrections = {
        'B': '8',
        'D': '0',
        'O': '0',
        'I': '1',
        'S': '5',
        'Z': '2',
        'A': '4'
    }
    return corrections.get(char, char)

def clean_vehicle_number(text: str):
    """
    Normalizes the detected text into the standard Army format using positional logic.
    Format: YY Class Serial Check
    """
    # Remove common noise
    candidate = text.replace("↑", "").replace("^", "").strip().upper()
    
    # Try to find the pattern
    match = ARMY_PLATE_PATTERN.search(candidate)
    if match:
        year_raw, class_raw, serial_raw, check_raw = match.groups()
        
        # 1. Year is always digits
        year = "".join([force_digit(c) for c in year_raw])
        
        # 2. Class is always a letter (This fixes 8 -> B)
        v_class = force_letter(class_raw)
        
        # 3. Serial is always digits
        serial = "".join([force_digit(c) for c in serial_raw])
        
        # 4. Check code is always a letter
        check = force_letter(check_raw)
        
        return f"{year}{v_class}{serial}{check}"
    
    # Fallback for non-standard reads
    fallback = re.sub(r"[^A-Z0-9]", "", candidate)
    if len(fallback) >= 7:
        return fallback
        
    return None

def run_ocr(image_path: str | Path):
    img = cv2.imread(str(image_path))
    if img is None:
        return None, 0.0

    results = get_reader().readtext(
        img,
        decoder="greedy",
        paragraph=False,
        detail=1,
        contrast_ths=0.1,
        adjust_contrast=0.7,
        add_margin=0.1,
        width_ths=0.7
    )

    # Combine fragments
    combined_text = " ".join([res[1] for res in results])
    cleaned = clean_vehicle_number(combined_text)
    
    if cleaned:
        best_conf = sum([res[2] for res in results]) / len(results) if results else 0.0
        return cleaned, float(best_conf)

    # Fallback: check individual fragments
    best_text = None
    best_conf = 0.0
    for _, text, confidence in results:
        cleaned = clean_vehicle_number(text)
        if cleaned and confidence > best_conf:
            best_text = cleaned
            best_conf = confidence

    return best_text, float(best_conf)
