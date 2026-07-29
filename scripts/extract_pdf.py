"""Usage examples for maro-processor with test-data PDFs."""

from pathlib import Path
from maro_processor.pdf import (
    PdfPlumberNativeEngine,
    PaddleOCREngine,
    SmartPDFExtractorRouter,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "test-data"

NATIVE_PDF = str(DATA_DIR / "25100512.pdf")
SCAN_PDF = str(DATA_DIR / "20251107105756329.pdf")


def demo_native_pipeline():
    """Run native extraction on a digital PDF, no OCR needed."""
    print("=" * 60)
    print("NATIVE PDF EXTRACTION")
    print("=" * 60)

    router = SmartPDFExtractorRouter(
        pdf_path=NATIVE_PDF,
        native_engine=PdfPlumberNativeEngine(),
    )

    print(f"Scanned? {router.detect_is_scanned()}")
    print()

    for page in router.process_document():
        print(f"--- Page {page.page_number} ({page.width:.0f}x{page.height:.0f}) ---")
        print(f"  Elements: {len(page.elements)}")

        text = page.to_layout_text(char_width=6.5, line_height=12.0)
        for line in text.splitlines()[:6]:
            print(f"  {line}")
        print()


def demo_ocr_pipeline():
    """Run OCR-based extraction on a scanned PDF."""
    print("=" * 60)
    print("SCANNED PDF EXTRACTION (OCR)")
    print("=" * 60)

    router = SmartPDFExtractorRouter(
        pdf_path=SCAN_PDF,
        native_engine=PdfPlumberNativeEngine(),
        ocr_engine=PaddleOCREngine.get_instance(),
    )

    print(f"Scanned? {router.detect_is_scanned()}")
    print()

    for page in router.process_document():
        print(f"--- Page {page.page_number} ({page.width:.0f}x{page.height:.0f}) ---")
        print(f"  Elements: {len(page.elements)}")

        text = page.to_layout_text(char_width=10.0, line_height=14.0)
        for line in text.splitlines()[:6]:
            print(f"  {line}")
        print()


def demo_spatial_elements():
    """Inspect raw spatial elements from both extraction paths."""
    print("=" * 60)
    print("SPATIAL ELEMENTS COMPARISON")
    print("=" * 60)

    native_engine = PdfPlumberNativeEngine()
    result = native_engine.extract_page(NATIVE_PDF, page_idx=0)
    print(f"\nNative — Page {result.page_number}:")
    for el in result.elements[:4]:
        print(f"  {el.text!r:30s}  x0={el.x0:6.1f}  y0={el.y0:6.1f}  x1={el.x1:6.1f}  y1={el.y1:6.1f}")

    ocr_engine = PaddleOCREngine.get_instance()
    result = ocr_engine.extract_page(SCAN_PDF, page_idx=0)
    print(f"\nOCR — Page {result.page_number}:")
    for el in result.elements[:4]:
        print(f"  {el.text!r:30s}  x0={el.x0:6.0f}  y0={el.y0:6.0f}  x1={el.x1:6.0f}  y1={el.y1:6.0f}  conf={el.confidence:.2f}")


if __name__ == "__main__":
    demo_native_pipeline()
    demo_ocr_pipeline()
    demo_spatial_elements()
