# maro-processor

`maro-processor` is a high-performance, multi-modal content intelligence platform built to transform unstructured media and documents into structured, production-ready assets. 

The core system handles complex data extraction pipelines locally, enforcing a **unified spatial JSON coordinate schema** across variable input tracks to guarantee data consistency for downstream AI, LLM, and database engines.

---

## Key Features

- **Intelligent PDF Routing:** Automatically analyzes document properties on-the-fly to detect whether a page contains native digital vectors or scanned raw pixels.
- **Unified Extraction API:** Enforces identical data structures (`PageExtractionResult`) regardless of the underlying extraction method used.
- **Spatial Layout Preservation:** Uses custom machine learning clusters (**DBSCAN**) and structural line regression (**RANSAC**) to automatically detect page skew, correct text rotation, and output perfectly tab-aligned layout strings.
- **Privacy-First & Air-Gapped:** Operates 100% locally on host hardware using optimized mobile model constraints. Zero data-tracking leak risks, zero recurring SaaS costs.

---

## Installation

`maro-processor` utilizes modular, light-weight entry footprints. Install only the exact processing dependencies your enterprise backend requires:

```bash
# Core & Native digital PDF parsing track only (Ultra-lightweight)
pip install maro-processor[pdf-native]

# Document suite complete with local spatial OCR fallbacks (Scanned documents & images)
pip install maro-processor[pdf-ocr]

# Full-stack deployment infrastructure (PDF + multi-modal engines)
pip install maro-processor[all]
```

---

## Quick Start (PDF Document Pipeline)

Here is a reproducible workflow example demonstrating how to run the multi-strategy document routing engine:

```python
from maro_processor.pdf import SmartPDFExtractorRouter, PdfPlumberNativeEngine, PaddleOCREngine

# 1. Initialize the intelligent router with pluggable extraction strategies
router = SmartPDFExtractorRouter(
    pdf_path="test-data/mixed_document.pdf",
    native_engine=PdfPlumberNativeEngine(),
    ocr_engine=PaddleOCREngine(), # Falls back cleanly if scanned layers are hit
)

print(f"Is scanned document template? {router.detect_is_scanned()}")

# 2. Iterate pages through the unified spatial extraction interface
for page in router.process_document():
    print(f"\n--- Page {page.page_number} ({page.width:.0f}x{page.height:.0f}) ---")
    print(f"Total Spatial Elements Tracked: {len(page.elements)}")
    
    # 3. Project raw coordinate segments into a clean, layout-preserved string
    structured_text = page.to_layout_text(char_width=6.5, line_height=12.0)
    print(structured_text)
```

---

## 📁 Repository Taxonomy

```text
src/maro_processor/
├── __init__.py         # Global distribution metadata
├── base.py             # Abstract structural execution contracts
├── schemas.py          # Unified Pydantic v2 spatial mapping structures
│
├── pdf/                # --- PDF & Document Extraction Sub-Module ---
│   ├── __init__.py     # Dependency safeguards & clean public imports
│   ├── router.py       # Intelligent heuristic routing engine
│   ├── native.py       # Local pdfplumber vector stream wrapper
│   ├── ocr.py          # Memory-optimized PaddleOCR mobile instance
│   └── utils.py        # DBSCAN spatial clustering & RANSAC skew
```

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` file for more details.

