from maro_processor.pdf.router import SmartPDFExtractorRouter
from maro_processor.pdf.native import PdfPlumberNativeEngine

try:
    from maro_processor.pdf.ocr import PaddleOCREngine
except ImportError:
    class PaddleOCREngine:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "PaddleOCREngine requires extra dependencies. "
                "Please install using: pip install maro-processor[pdf-ocr]"
            )

__all__ = [
    "SmartPDFExtractorRouter",
    "PdfPlumberNativeEngine",
    "PaddleOCREngine",
]

