# Doc-Sort AI (Gen 2.0) - Phase 1 Implementation

This repository contains the initial implementation of the Doc-Sort AI platform.

## Structure

*   `backend/`: Node.js Fastify server for API handling.
*   `ai_engine/`: Python scripts for OCR simulation and document processing.

## Prerequisites

*   Node.js (v18+)
*   Python (3.8+)
*   `pip` and `npm`

## Setup

1.  **Backend Setup:**
    ```bash
    cd backend
    npm install
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

## Features Implemented (Phase 1)

*   **Fast-Pass Check (FR-1.2):** Basic metadata extraction and page count.
*   **Dual-Pathway OCR Simulation (FR-1.3):** Simulates routing to Tesseract (CPU) or DeepSeek (GPU) based on content complexity.
*   **Splitting Engine Simulation (FR-2.1):** Simulates document splitting and grouping based on visual heuristics.
