"""Structural validation tests for maro-processor extraction pipeline."""

from pathlib import Path
from maro_processor.schemas import SpatialTextElement, PageExtractionResult


PDF_DIR = Path(__file__).resolve().parent.parent / "test-data"


def test_spatial_element_creation():
    el = SpatialTextElement(text="Hello", x0=0.0, y0=0.0, x1=50.0, y1=12.0)
    assert el.text == "Hello"
    assert el.x0 == 0.0
    assert el.y1 == 12.0
    assert el.confidence is None


def test_spatial_element_with_confidence():
    el = SpatialTextElement(text="OCR", x0=10.0, y0=20.0, x1=60.0, y1=30.0, confidence=0.95)
    assert el.confidence == 0.95


def test_page_result_empty_to_layout_text():
    result = PageExtractionResult(page_number=1, width=500.0, height=800.0, is_ocr=False)
    assert result.to_layout_text() == ""


def test_page_result_to_layout_text():
    result = PageExtractionResult(page_number=1, width=500.0, height=800.0, is_ocr=False)
    result.elements = [
        SpatialTextElement(text="Hello", x0=0.0, y0=0.0, x1=40.0, y1=14.0),
        SpatialTextElement(text="World", x0=80.0, y0=0.0, x1=130.0, y1=14.0),
    ]
    text = result.to_layout_text(char_width=10.0, line_height=14.0)
    assert "Hello" in text
    assert "World" in text


def test_page_result_multiline():
    result = PageExtractionResult(page_number=1, width=500.0, height=800.0, is_ocr=False)
    result.elements = [
        SpatialTextElement(text="Line1", x0=0.0, y0=0.0, x1=45.0, y1=14.0),
        SpatialTextElement(text="Line2", x0=0.0, y0=20.0, x1=45.0, y1=34.0),
    ]
    text = result.to_layout_text(char_width=10.0, line_height=14.0)
    lines = text.splitlines()
    assert len(lines) == 2
    assert "Line1" in lines[0]
    assert "Line2" in lines[1]


def test_native_extraction():
    pdf_path = PDF_DIR / "25100512.pdf"
    if not pdf_path.exists():
        return

    from maro_processor.pdf.native import PdfPlumberNativeEngine

    engine = PdfPlumberNativeEngine()
    result = engine.extract_page(str(pdf_path), page_idx=0)

    assert result.page_number == 1
    assert result.width > 0
    assert result.height > 0
    assert result.is_ocr is False
    assert len(result.elements) > 0
    assert any("SOGEDIAL" in el.text for el in result.elements)


def test_router_native():
    pdf_path = PDF_DIR / "25100512.pdf"
    if not pdf_path.exists():
        return

    from maro_processor.pdf.router import SmartPDFExtractorRouter
    from maro_processor.pdf.native import PdfPlumberNativeEngine

    router = SmartPDFExtractorRouter(
        pdf_path=str(pdf_path),
        native_engine=PdfPlumberNativeEngine(),
    )

    assert router.detect_is_scanned() is False

    pages = list(router.process_document())
    assert len(pages) == 3
    for p in pages:
        assert p.is_ocr is False


def test_ocr_extraction():
    pdf_path = PDF_DIR / "20251107105756329.pdf"
    if not pdf_path.exists():
        return

    try:
        from maro_processor.pdf.ocr import PaddleOCREngine
    except ImportError:
        return

    engine = PaddleOCREngine()
    result = engine.extract_page(str(pdf_path), page_idx=0)

    assert result.page_number == 1
    assert result.width > 0
    assert result.height > 0
    assert result.is_ocr is True
    assert len(result.elements) > 0


def test_router_ocr():
    pdf_path = PDF_DIR / "20251107105756329.pdf"
    if not pdf_path.exists():
        return

    try:
        from maro_processor.pdf.ocr import PaddleOCREngine
        from maro_processor.pdf.router import SmartPDFExtractorRouter
        from maro_processor.pdf.native import PdfPlumberNativeEngine
    except ImportError:
        return

    router = SmartPDFExtractorRouter(
        pdf_path=str(pdf_path),
        native_engine=PdfPlumberNativeEngine(),
        ocr_engine=PaddleOCREngine(),
    )

    assert router.detect_is_scanned() is True

    pages = list(router.process_document())
    assert len(pages) == 3
    for p in pages:
        assert p.is_ocr is True
        assert len(p.elements) > 0
