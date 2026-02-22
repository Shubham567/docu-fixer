# Doc-Sort AI (Gen 2.0) - Advanced Implementation

This repository contains the advanced implementation of the Doc-Sort AI platform.

## Structure

*   `backend/`: Node.js Fastify server for API handling.
*   `ai_engine/`: Python package for OCR and Intelligent Splitting.
    *   `ocr.py`: Handles text extraction and OCR routing (simulated Tesseract/DeepSeek).
    *   `splitter.py`: Implements Semantic Splitting using `sentence-transformers` (S-BERT).
    *   `main.py`: Entry point for processing.
    *   `tests/`: Unit tests for the AI components.

## Prerequisites

*   Node.js (v18+)
*   Python (3.8+)
*   `pip` and `npm`

## Setup

1.  **Backend Setup:**
    ```bash
    cd backend
    npm install
    cp .env.example .env
    ```

2.  **AI Engine Setup:**
    ```bash
    pip install -r ai_engine/requirements.txt
    ```

## Running the Application

1.  Start the backend server:
    ```bash
    cd backend
    npm start
    ```
    The server will start on `http://localhost:3000`.

2.  Upload a document:
    Use `curl` or Postman to upload a PDF file to `http://localhost:3000/upload`.

    Example:
    ```bash
    curl -X POST -F "file=@/path/to/document.pdf" http://localhost:3000/upload
    ```

## Running Tests

To run the AI Engine unit tests:
```bash
python3 -m unittest discover -s ai_engine/tests -t .
```

## Features Implemented

*   **Production-Ready Structure:** Modular Python code, Environment variables, Logging.
*   **Semantic Splitting (FR-2.2):** Uses `sentence-transformers` to calculate cosine similarity between pages and automatically group them based on topic coherence.
*   **Hybrid OCR Routing (FR-1.3):** Intelligent fallback from Text Layer Extraction to Tesseract (simulated if binary missing) to DeepSeek (simulated/placeholder).
*   **Robust Backend:** Fastify with `pino` logging, file type validation, and error handling.
