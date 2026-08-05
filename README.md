# maro-processor

![PyPI Version](https://img.shields.io/pypi/v/maro-processor)

`maro-processor` is a Python tool that helps you extract text and tables from PDFs. It works on both digital PDFs and scanned images.

If a PDF has clean digital text, it reads it instantly. If the PDF is a scanned image or photo, it automatically switches to OCR mode. It also uses algorithms (**DBSCAN** and **RANSAC**) to straighten crooked pages and keep your columns and text layout perfectly aligned.

---

## Features

- **Automatic Detection:** Automatically checks if your PDF has real text or if it is just a scanned image.
- **Unified Output:** Gives you the exact same data structure (`PageExtractionResult`) whether it used native reading or OCR fallback.
- **Layout Fixes:** Automatically straightens rotated pages and keeps text columns aligned using spatial clustering.
- **100% Private & Local:** Everything runs entirely on your own computer. No data leaks, no cloud API bills.

---

## Installation

You can install only the modules you need to save disk space:

```bash
# Digital PDFs only (Very lightweight)
pip install maro-processor[pdf-native]

# Digital + Scanned PDFs (Includes PaddleOCR and machine learning models)
pip install maro-processor[pdf-ocr]

# Full package
pip install maro-processor[all]
```

---

## Quick Start

Here is how to process a PDF file automatically:

```python
from maro_processor.pdf import SmartPDFExtractorRouter, PdfPlumberNativeEngine, PaddleOCREngine

# Initialize the router with your extraction tools
router = SmartPDFExtractorRouter(
    pdf_path="invoice.pdf",
    native_engine=PdfPlumberNativeEngine(),
    ocr_engine=PaddleOCREngine(), # Falls back to OCR if the file is an image
)

print(f"Is this a scanned document? {router.detect_is_scanned()}")

# Process your document page by page
for page in router.process_document():
    print(f"\n--- Page {page.page_number} ({page.width:.0f}x{page.height:.0f}) ---")
    
    # Converts absolute coordinates into a readable text layout string
    text = page.to_layout_text(char_width=6.5, line_height=12.0)
    print(text)
```

---

## Project Structure

```text
src/maro_processor/
├── __init__.py         # Package version and metadata
├── base.py             # Core engine interfaces
├── schemas.py          # Pydantic data models for coordinate storage
│
├── pdf/                # --- PDF Sub-Module ---
│   ├── __init__.py     # Clean imports and fallback checks
│   ├── router.py       # Scanned vs digital detection logic
│   ├── native.py       # Wrapper for pdfplumber
│   ├── ocr.py          # Memory-optimized PaddleOCR engine
│   └── utils.py        # DBSCAN row sorting and RANSAC angle fixing
```

---

## License

Distributed under the **MIT License**. See the `LICENSE` file in this repository for more details.


