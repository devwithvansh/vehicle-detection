from pathlib import Path
import cv2
import numpy as np

def enhance_for_ocr(image):
    """
    Applies multiple enhancement techniques to improve OCR on blurry or low-contrast images.
    """
    # 1. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Rescaling (DPI increase simulation)
    # Doubling the size often helps EasyOCR with small or blurry text
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 3. CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # 4. Denoising while preserving edges
    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
    
    # 5. Unsharp Masking (Sharpening)
    gaussian_blur = cv2.GaussianBlur(denoised, (0, 0), 3)
    sharpened = cv2.addWeighted(denoised, 1.5, gaussian_blur, -0.5, 0)
    
    return sharpened

def preprocess_plate_image(input_path: str | Path, output_path: str | Path) -> str:
    """
    Advanced preprocessing for army plates, especially for blurry/shaky captures.
    """
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError("Unable to read image")

    h, w = image.shape[:2]
    
    # Dynamic Crop: Army plates are often on the front bumper or rear.
    # Instead of a very tight crop, we take a generous middle-lower section 
    # to ensure we don't cut off the arrow or check digit.
    # For blurry images, having more context sometimes helps the OCR engine.
    crop = image[int(h * 0.2):int(h * 0.9), int(w * 0.05):int(w * 0.95)]
    
    # Apply enhancements
    processed = enhance_for_ocr(crop)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the processed image
    cv2.imwrite(str(output_path), processed)

    return str(output_path)
