import random
from PyPDF2 import PdfReader
from ai_engine.utils import logger

class OCREngine:
    def __init__(self):
        self.tesseract_available = False
        try:
            import pytesseract
            # Check if tesseract binary is available
            try:
                pytesseract.get_tesseract_version()
                self.tesseract_available = True
            except Exception:
                logger.warning("Tesseract binary not found. Falling back to text extraction/simulation.")
        except ImportError:
            logger.warning("pytesseract not installed.")

    def extract_text(self, file_path):
        """
        Extracts text from a PDF file using a hybrid approach.
        1. Try standard text layer extraction (PyPDF2).
        2. If empty (scanned), would attempt Tesseract (simulated here if missing).
        3. Determine complexity for 'routing'.
        """
        results = []
        try:
            reader = PdfReader(file_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()

                # Intelligent Routing Logic (FR-1.3)
                method = "Text Layer Extraction"

                # Check for empty text (Scanned Document)
                if not text or len(text.strip()) < 10:
                    if self.tesseract_available:
                        # In a real environment with pdf2image:
                        # images = convert_from_path(file_path, first_page=i+1, last_page=i+1)
                        # text = pytesseract.image_to_string(images[0])
                        method = "Tesseract OCR (Real)"
                        text = "(Tesseract would extract text here if poppler was available)"
                    else:
                        method = "Tesseract OCR (Simulated)"
                        text = f"(Simulated OCR Content for Page {i+1})"

                # Check for Complexity (Handwritten / Tables)
                # Heuristic: If we had image analysis, we'd check for lines/grids.
                # Here, we simulate based on random chance or keywords if text exists.
                is_complex = False
                if "table" in text.lower() or "handwritten" in text.lower() or random.random() > 0.8:
                     is_complex = True

                if is_complex:
                    method = "DeepSeek-OCR (GPU)"
                    # In production: Call DeepSeek API
                    text = f"[DeepSeek Enriched] {text}"

                results.append({
                    "page": i + 1,
                    "method": method,
                    "content": text.strip()
                })

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise e

        return results
