from maro_processor.pdf.router import SmartPDFExtractorRouter
from maro_processor.pdf.native import PdfPlumberNativeEngine

__all__ = [
    "SmartPDFExtractorRouter",
    "PdfPlumberNativeEngine",
    "PaddleOCREngine",
]


def __getattr__(name):
    if name == "PaddleOCREngine":
        try:
            from maro_processor.pdf.ocr import PaddleOCREngine
        except ImportError as exc:
            raise ImportError(
                "PaddleOCREngine requires the 'pdf-ocr' extras: "
                "pip install maro-processor[pdf-ocr]"
            ) from exc
        return PaddleOCREngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

