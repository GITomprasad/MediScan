"""
MediScan AI - Document Processing Service
Handles PDF extraction (PyMuPDF) and Image OCR (RapidOCR + pytesseract fallback).
Validates file types, sizes, and extracted text quality.
"""

import io
import os
import re
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Initialize RapidOCR engine
_rapid_ocr = None

def get_rapid_ocr():
    global _rapid_ocr
    if _rapid_ocr is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _rapid_ocr = RapidOCR()
        except Exception as e:
            print(f"[DocumentService] Could not initialize RapidOCR: {e}")
            _rapid_ocr = False
    return _rapid_ocr if _rapid_ocr is not False else None

def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """Preprocess image for better OCR character recognition."""
    # Convert to grayscale
    gray = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray)
    contrast_img = enhancer.enhance(1.8)
    # Mild sharpening
    sharpened = contrast_img.filter(ImageFilter.SHARPEN)
    return sharpened

def run_ocr_on_image(image: Image.Image) -> str:
    """Run OCR on a PIL Image using RapidOCR with pytesseract fallback."""
    text_fragments = []
    
    # 1. Try RapidOCR (high accuracy ONNX model)
    ocr_engine = get_rapid_ocr()
    if ocr_engine is not None:
        try:
            # RapidOCR accepts PIL Image or numpy array
            import numpy as np
            img_np = np.array(image)
            result, _ = ocr_engine(img_np)
            if result:
                for line in result:
                    # line format: [box_coordinates, text, confidence]
                    if len(line) >= 2 and line[1]:
                        text_fragments.append(line[1].strip())
        except Exception as ex:
            print(f"[DocumentService] RapidOCR run warning: {ex}")

    # 2. If RapidOCR returned little text, try pytesseract as fallback
    if len(" ".join(text_fragments).strip()) < 20:
        try:
            import pytesseract
            # Check standard UB-Mannheim tesseract path if not on PATH
            if not pytesseract.pytesseract.tesseract_cmd or pytesseract.pytesseract.tesseract_cmd == 'tesseract':
                common_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
                ]
                for p in common_paths:
                    if os.path.exists(p):
                        pytesseract.pytesseract.tesseract_cmd = p
                        break
            
            prep_img = preprocess_image_for_ocr(image)
            tess_text = pytesseract.image_to_string(prep_img)
            if tess_text and len(tess_text.strip()) > len(" ".join(text_fragments)):
                return tess_text.strip()
        except Exception:
            pass

    return "\n".join(text_fragments).strip()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF; fallback to OCR if scanned/image-only."""
    extracted_text = []
    
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")

    page_count = len(doc)
    if page_count == 0:
        doc.close()
        raise ValueError("PDF document contains no pages.")

    # Step 1: Attempt digital text extraction
    for page_num in range(page_count):
        page = doc[page_num]
        page_text = page.get_text("text").strip()
        if page_text:
            extracted_text.append(page_text)

    combined_text = "\n\n".join(extracted_text).strip()

    # Step 2: If selectable text is insufficient (< 30 characters), run OCR on rendered page images
    if len(combined_text) < 30:
        ocr_texts = []
        # Process up to 5 pages for efficiency and speed
        max_ocr_pages = min(page_count, 5)
        for page_num in range(max_ocr_pages):
            page = doc[page_num]
            # Render page to high-res image (2x zoom = 144 DPI)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_ocr = run_ocr_on_image(img)
            if page_ocr:
                ocr_texts.append(page_ocr)
        
        combined_text = "\n\n".join(ocr_texts).strip()

    doc.close()
    return combined_text

def extract_text_from_image(file_path: str) -> str:
    """Extract text from an image file using OCR."""
    try:
        with Image.open(file_path) as img:
            # Convert palette/RGBA to RGB
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            return run_ocr_on_image(img)
    except Exception as e:
        raise ValueError(f"Failed to open or process image file: {str(e)}")

def process_document(file_path: str, filename: str) -> str:
    """Process document file and return extracted text with quality checks."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {filename}")

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValueError("The uploaded file is empty (0 bytes).")
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds maximum allowed size of 10MB.")

    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file format '{ext}'. Allowed: PDF, PNG, JPG, JPEG.")

    if ext == 'pdf':
        raw_text = extract_text_from_pdf(file_path)
    else:
        raw_text = extract_text_from_image(file_path)

    # Validate extracted text quality
    cleaned = raw_text.strip()
    words = re.findall(r'[a-zA-Z]{2,}', cleaned)
    
    if len(cleaned) < 25 or len(words) < 4:
        raise ValueError(
            "Insufficient extracted text: The document appears blank, blurry, or contains no decipherable medical text. "
            "Please upload a clear, legible medical document."
        )

    return cleaned
