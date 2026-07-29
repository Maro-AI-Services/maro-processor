import pdfplumber
from maro_processor.base import BaseExtractorEngine
from maro_processor.schemas import PageExtractionResult, SpatialTextElement


class PdfPlumberNativeEngine(BaseExtractorEngine):
    def extract_page(self, file_source: str, page_idx: int, **kwargs) -> PageExtractionResult:
        with pdfplumber.open(file_source) as pdf:
            page = pdf.pages[page_idx]
            result = PageExtractionResult(
                page_number=page_idx + 1,
                width=float(page.width),
                height=float(page.height),
                is_ocr=False,
            )

            words = page.extract_words()
            for w in words:
                result.elements.append(SpatialTextElement(
                    text=w["text"],
                    x0=float(w["x0"]),
                    y0=float(w["top"]),
                    x1=float(w["x1"]),
                    y1=float(w["bottom"]),
                ))

            return result
