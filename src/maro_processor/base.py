from abc import ABC, abstractmethod
from typing import Any
from maro_processor.schemas import PageExtractionResult


class BaseExtractorEngine(ABC):
    @abstractmethod
    def extract_page(self, file_source: Any, page_idx: int, **kwargs) -> PageExtractionResult:
        pass
