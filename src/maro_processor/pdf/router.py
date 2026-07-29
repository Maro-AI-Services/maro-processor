import pdfplumber
from typing import Generator, Optional
from maro_processor.base import BaseExtractorEngine
from maro_processor.pdf.native import PdfPlumberNativeEngine
from maro_processor.schemas import PageExtractionResult


class SmartPDFExtractorRouter:
    def __init__(
        self,
        pdf_path: str,
        native_engine: Optional[BaseExtractorEngine] = None,
        ocr_engine: Optional[BaseExtractorEngine] = None,
    ):
        self.pdf_path = pdf_path
        self.native_engine = native_engine or PdfPlumberNativeEngine()
        self.ocr_engine = ocr_engine

    def detect_is_scanned(self, text_threshold: int = 15) -> bool:
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                if not pdf.pages:
                    return True
                first_page_text = pdf.pages[0].extract_text() or ""
                return len(first_page_text.strip()) < text_threshold
        except Exception:
            return True

    def process_document(self) -> Generator[PageExtractionResult, None, None]:
        is_scanned = self.detect_is_scanned()
        selected_engine = self.ocr_engine if is_scanned else self.native_engine

        if is_scanned and not self.ocr_engine:
            raise ValueError(
                "Pipeline Error: Document is scanned, but no OCR engine class was provided."
            )

        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)

        for idx in range(total_pages):
            yield selected_engine.extract_page(self.pdf_path, page_idx=idx)
