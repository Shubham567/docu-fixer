import unittest
from unittest.mock import MagicMock, patch
from ai_engine.ocr import OCREngine

class TestOCREngine(unittest.TestCase):
    def setUp(self):
        self.ocr = OCREngine()

    @patch('ai_engine.ocr.PdfReader')
    def test_extract_text_standard(self, MockPdfReader):
        # Setup mock
        mock_reader = MockPdfReader.return_value
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "This is standard text content."
        mock_reader.pages = [mock_page]

        results = self.ocr.extract_text("dummy.pdf")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["method"], "Text Layer Extraction")
        self.assertEqual(results[0]["content"], "This is standard text content.")

    @patch('ai_engine.ocr.PdfReader')
    def test_extract_text_empty(self, MockPdfReader):
        # Simulate scanned PDF (empty text)
        mock_reader = MockPdfReader.return_value
        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""
        mock_reader.pages = [mock_page]

        # Mock tesseract check
        self.ocr.tesseract_available = False

        results = self.ocr.extract_text("dummy.pdf")

        self.assertEqual(results[0]["method"], "Tesseract OCR (Simulated)")
        self.assertIn("Simulated OCR Content", results[0]["content"])

if __name__ == '__main__':
    unittest.main()
