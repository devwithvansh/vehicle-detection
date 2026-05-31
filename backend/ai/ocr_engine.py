import re
import cv2
import easyocr
import numpy as np
from functools import lru_cache
from pathlib import Path

# =============================================================================
# INDIAN ARMY VEHICLE PLATE OCR ENGINE
# =============================================================================
# This module handles the extraction and normalization of Indian Army vehicle
# license plates. It uses EasyOCR for text extraction and applies custom
# positional logic to correct common OCR misinterpretations.
#
# Format: [Arrow] [Year: 2 digits] [Class: 1 letter] [Serial: 5-7 digits] [Check: 1 letter]
# Example: ↑64B087985E
# =============================================================================

# Updated pattern to be more flexible for noisy reads and various symbols
# It captures Year, Class, Serial, and Check code as groups.
ARMY_PLATE_PATTERN = re.compile(r"(?:[↑\^1T7IL]\s*)?(\d{2})\s*([A-Z0-9])\s*(\d{4,8})\s*([A-Z0-9])")

@lru_cache
def get_reader():
    """
    Returns a cached instance of the EasyOCR Reader.
    Using 'en' for English alphanumeric characters.
    """
    return easyocr.Reader(["en"], gpu=False)

def force_letter(char: str) -> str:
    """
    Corrects common OCR digit-to-letter misinterpretations based on 
    visual similarity. This is used for positions where a letter is expected.
    """
    corrections = {
        '0': 'D',
        '1': 'I',
        '2': 'Z',
        '4': 'A',
        '5': 'S',
        '6': 'G',
        '8': 'B',
        '9': 'P'
    }
    return corrections.get(char, char.upper())

def force_digit(char: str) -> str:
    """
    Corrects common OCR letter-to-digit misinterpretations based on
    visual similarity. This is used for positions where a digit is expected.
    """
    corrections = {
        'A': '4',
        'B': '8',
        'D': '0',
        'G': '6',
        'I': '1',
        'L': '1',
        'O': '0',
        'S': '5',
        'T': '7',
        'Z': '2'
    }
    return corrections.get(char, char)

def clean_vehicle_number(text: str):
    """
    Normalizes the detected text into the standard Army format using positional logic.
    Ensures the arrow is prepended without a space.
    
    Args:
        text (str): The raw text extracted by OCR.
        
    Returns:
        str: The formatted plate number (e.g., ↑64B087985E) or None if invalid.
    """
    if not text:
        return None

    # Step 1: Remove common noise and normalize to uppercase
    # We strip the arrow and caret to process the core alphanumeric sequence.
    candidate = text.replace("↑", "").replace("^", "").strip().upper()
    
    # Step 2: Try to match the standard Army plate pattern
    match = ARMY_PLATE_PATTERN.search(candidate)
    if match:
        year_raw, class_raw, serial_raw, check_raw = match.groups()
        
        # 1. Year is always 2 digits
        year = "".join([force_digit(c) for c in year_raw])
        
        # 2. Class is always a single letter (e.g., B, A, X)
        v_class = force_letter(class_raw)
        
        # 3. Serial is a sequence of digits (usually 5-7)
        serial = "".join([force_digit(c) for c in serial_raw])
        
        # 4. Check code is always a trailing letter
        check = force_letter(check_raw)
        
        # Format: Arrow + Year + Class + Serial + Check (No Spaces)
        return f"↑{year}{v_class}{serial}{check}"
    
    # Step 3: Fallback for non-standard or fragmented reads
    # If the regex fails, we strip everything except letters and digits.
    fallback = re.sub(r"[^A-Z0-9]", "", candidate)
    
    # Minimum length for a valid army plate is usually around 8-10 chars
    if len(fallback) >= 6:
        return f"↑{fallback}"
        
    return None

def perform_ocr_on_image(img):
    """
    Helper function to run EasyOCR on a numpy image array.
    """
    reader = get_reader()
    results = reader.readtext(
        img,
        decoder="greedy",
        paragraph=False,
        detail=1,
        contrast_ths=0.1,
        adjust_contrast=0.7,
        add_margin=0.1,
        width_ths=0.7
    )
    return results

def run_ocr(image_path: str | Path):
    """
    Main entry point for OCR. Performs a multi-pass analysis to improve
    recognition in blurry or low-light conditions.
    
    Args:
        image_path (str | Path): Path to the image file.
        
    Returns:
        tuple: (detected_number, confidence_score)
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return None, 0.0

    # Pass 1: Original Processed Image
    results = perform_ocr_on_image(img)
    
    # Combine fragments from the first pass
    combined_text = " ".join([res[1] for res in results])
    cleaned = clean_vehicle_number(combined_text)
    
    if cleaned:
        # Calculate average confidence
        best_conf = sum([res[2] for res in results]) / len(results) if results else 0.0
        return cleaned, float(best_conf)

    # Pass 2: Fallback - check individual fragments from the first pass
    best_text = None
    best_conf = 0.0
    for _, text, confidence in results:
        cleaned = clean_vehicle_number(text)
        if cleaned and confidence > best_conf:
            best_text = cleaned
            best_conf = confidence

    if best_text:
        return best_text, float(best_conf)

    # Pass 3: Multi-thresholding for very blurry/shaky images
    # We try a slightly different preprocessing if the first pass failed
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    results_v2 = perform_ocr_on_image(thresh)
    combined_text_v2 = " ".join([res[1] for res in results_v2])
    cleaned_v2 = clean_vehicle_number(combined_text_v2)
    
    if cleaned_v2:
        conf_v2 = sum([res[2] for res in results_v2]) / len(results_v2) if results_v2 else 0.0
        return cleaned_v2, float(conf_v2)

    return None, 0.0

# =============================================================================
# END OF MODULE
# =============================================================================
