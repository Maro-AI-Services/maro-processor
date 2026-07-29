# maro-processor

Hybrid Native & OCR PDF Layout Extraction Engine.

## Installation

```bash
# PDF native extraction only (lightweight)
pip install maro-processor[pdf-native]

# PDF native + OCR fallback (for scanned documents)
pip install maro-processor[pdf-ocr]

# Full suite
pip install maro-processor[all]
```

## Usage

```python
from maro_processor.pdf import SmartPDFExtractorRouter, PdfPlumberNativeEngine, PaddleOCREngine

router = SmartPDFExtractorRouter(
    pdf_path="document.pdf",
    native_engine=PdfPlumberNativeEngine(),
    ocr_engine=PaddleOCREngine(),
)
for page in router.process_document():
    print(page.to_layout_text())
```

## Structure

```
src/maro_processor/
├── __init__.py
├── base.py
├── schemas.py
├── pdf/
│   ├── router.py
│   ├── native.py
│   ├── ocr.py
│   └── utils.py
```
