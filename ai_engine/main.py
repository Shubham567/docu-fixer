import sys
import json
import os
from ai_engine.ocr import OCREngine
from ai_engine.splitter import SplitterEngine
from ai_engine.utils import logger

def process_document(file_path):
    logger.info(f"Starting processing for: {file_path}")

    # Initialize Engines
    try:
        ocr_engine = OCREngine()
        splitter_engine = SplitterEngine() # Uses SentenceTransformer by default
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return {"status": "error", "message": str(e)}

    # 1. OCR / Text Extraction
    try:
        pages_data = ocr_engine.extract_text(file_path)
        logger.info(f"Extracted text from {len(pages_data)} pages.")
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return {"status": "error", "message": str(e)}

    # 2. Intelligent Splitting
    try:
        groups = splitter_engine.split_document(pages_data)
        logger.info(f"Document split into {len(groups)} logical groups.")
    except Exception as e:
        logger.error(f"Splitting failed: {e}")
        # Fallback: One group per page
        groups = [{"group_id": i+1, "pages": [p["page"]], "classification": "Error"} for i, p in enumerate(pages_data)]

    return {
        "status": "success",
        "metadata": {
            "page_count": len(pages_data),
            "processed_files": [file_path]
        },
        "ocr_results": pages_data,
        "document_groups": groups
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No file path provided"}))
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": "File not found"}))
        sys.exit(1)

    result = process_document(file_path)
    print(json.dumps(result, indent=2))
