# Business Requirements Document (BRD): AI-Powered Document Page Sorting & Intelligent Grouping

## 1. Document Overview
* **Project Name:** Doc-Sort AI (Gen 2.0)
* **Version:** 1.0.0
* **Status:** Draft / Ready for Engineering Review
* **Target Markets:** Indian Judiciary (E-Courts), Indian SMEs (GST Compliance), Enterprise Legal/HR.

---

## 2. Executive Summary
This project aims to solve the "Jumbled PDF" crisis by developing a multimodal AI platform that autonomously splits, reorders, and groups disorganized document scans. Unlike legacy OCR, this platform utilizes LLMs, Computer Vision, and Graph Convolutional Networks (GCNs) to understand document boundaries and semantic flow, ensuring compliance with India's DPDPA 2023.

---

## 3. Functional Requirements

### 3.1 Multimodal Ingestion & Pre-processing
* **FR-1.1: Omnichannel Ingestion:** Support for bulk PDF uploads via API, Email, and Web Portal.
* **FR-1.2: Lightweight Fast-Pass:** Initial heuristic check for file metadata and page count to optimize routing.
* **FR-1.3: Dual-Pathway OCR Routing:**
    * **Pathway A (Standard):** Tesseract OCR for clean, machine-printed text (CPU-based).
    * **Pathway B (Complex):** DeepSeek-OCR for tabular data, hand-written notes, and mixed scripts (GPU-based).



### 3.2 Intelligent Boundary Detection & Reordering
* **FR-2.1: Visual Boundary Detection:** Identification of logos, signature blocks, and layout shifts using Computer Vision.
* **FR-2.2: Semantic Coherence Scoring:** * Implementation of **Topic Coherence with Embeddings (TCE)** using S-BERT.
    * Application of **METEOR Metrics** to ensure narrative continuity in legal/narrative documents.
* **FR-2.3: Structural Mapping:** Use of **Graph Convolutional Networks (GCNs)** to maintain table integrity across page breaks.

### 3.3 Data Extraction & Normalization
* **FR-3.1: Template-Free Extraction:** Use of RAG (Retrieval-Augmented Generation) to extract fields (GSTIN, Invoice #, Case ID) without fixed coordinates.
* **FR-3.2: Data Normalization:** Standardizing dates, currencies, and HSN/SAC codes into a unified schema.

### 3.4 Human-in-the-Loop (HITL) Interface
* **FR-4.1: Confidence Thresholding:** Flagging documents with <85% confidence for manual review.
* **FR-4.2: "Show Highlight" Diagnostic:** UI must snap to the specific bounding box/paragraph of the flagged error.
* **FR-4.3: Feedback Loop:** Manual corrections must trigger incremental model retraining (Reinforcement Learning).

---

## 4. Technical Architecture

| Layer | Component | Technology Stack |
| :--- | :--- | :--- |
| **Infrastructure** | Cloud/On-Prem | Docker, Kubernetes, NVIDIA GPU Clusters |
| **OCR Engine** | Hybrid Routing | Tesseract (Open Source), DeepSeek-OCR |
| **LLM / Semantic** | Reasoning & Scoring | Sentence-BERT, Llama 3 (Self-hosted), RoBERTa |
| **Database** | Metadata & Vector | PostgreSQL (pgvector), Redis |
| **Backend** | API & Orchestration | Fastify, Python (PyTorch), Prisma |

---

## 5. Regulatory Compliance (DPDPA 2023)

* **CP-1.1: Consent Management:** Standalone, granular notice generation before data processing.
* **CP-1.2: Data Localization:** Ability to deploy as an air-gapped solution to keep sensitive data within Indian borders.
* **CP-1.3: PII Redaction:** Automatic masking of Aadhaar and PAN numbers during the "Review" stage.
* **CP-1.4: Erasure Protocol:** Instant data purging upon revocation of consent via API.

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
* Deployment of self-hosted Tesseract and DeepSeek-OCR.
* Development of the basic PDF splitting engine based on visual heuristics.

### Phase 2: Intelligence (Months 4-6)
* Integration of S-BERT for TCE (Coherence) scoring.
* Implementation of GCNs for complex table reconstruction.

### Phase 3: Compliance & UI (Months 7-9)
* Build DPDPA-compliant consent modules.
* Launch "Show Highlight" HITL dashboard.

### Phase 4: Scaling & Integration (Months 10-12)
* ERP/Accounting software integrations (Tally, SAP, Oracle).
* On-boarding for E-Courts pilot program.

---

## 7. Monetization Logic

* **Tier 1 (Freemium):** Limited to 50 pages/month; Basic OCR only.
* **Tier 2 (Usage-Based):** $0.05 per page; includes Semantic Reordering; target SMEs.
* **Tier 3 (Enterprise):** Annual Licensing + SLA; On-premise deployment; target Law Firms & Judiciary.

---

## 8. Success Metrics (KPIs)
* **Accuracy:** >98% boundary detection accuracy.
* **Speed:** <5 seconds processing time for a 50-page jumbled document.
* **Efficiency:** 60% reduction in manual document sorting hours for clients.
