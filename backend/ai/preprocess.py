from pathlib import Path
import cv2
import numpy as np

def preprocess_plate_image(input_path: str | Path, output_path: str | Path) -> str:
    """
    Optimized preprocessing for painted army plates:
    1. Adaptive cropping (if possible) or just focus on central area.
    2. CLAHE for contrast enhancement (good for painted numbers).
    3. Bilateral filter to reduce noise while keeping edges sharp.
    """
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError("Unable to read image")

    h, w = image.shape[:2]
    
    # Army plates are often on bumpers. The original crop was too aggressive.
    # Let's use a slightly wider crop or dynamic detection if we had a model, 
    # but for now, we'll refine the static crop to be more inclusive.
    crop = image[int(h * 0.3):int(h * 0.8), int(w * 0.1):int(w * 0.9)]
    
    # Convert to grayscale
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # 1. Contrast Enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This is excellent for painted numbers which might have low contrast with the background.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 2. Denoising while preserving edges
    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

    # 3. Sharpening
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # 4. Thresholding (Adaptive is usually better for varying lighting)
    thresh = cv2.adaptiveThreshold(
        sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the processed image
    # We save the 'enhanced' or 'sharpened' version for OCR as EasyOCR 
    # often performs better on grayscale than on hard binary thresholds.
    cv2.imwrite(str(output_path), sharpened)

    return str(output_path)
