import os
import threading

os.environ.setdefault("FLAGS_use_mkldnn", "0")
os.environ.setdefault("MKLDNN_CACHE_CAPACITY", "0")

import cv2
import numpy as np
import paddle
import pdfplumber
from paddleocr import PaddleOCR

from maro_processor.base import BaseExtractorEngine
from maro_processor.schemas import PageExtractionResult, SpatialTextElement


paddle.set_flags({
    "FLAGS_fraction_of_cpu_memory_to_use": 0.15,
    "FLAGS_allocator_strategy": "naive_best_fit",
    "FLAGS_eager_delete_scope": True,
    "FLAGS_fast_eager_deletion_mode": True,
})

try:
    from paddle.fluid.core import set_mkldnn_cache_capacity
    set_mkldnn_cache_capacity(10)
except ImportError:
    pass


class PaddleOCREngine(BaseExtractorEngine):
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, lang: str = "fr"):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(lang)
        return cls._instance

    def __init__(self, lang: str = "fr"):
        self.lang = lang
        self.ocr = PaddleOCR(
            lang=lang,
            ocr_version="PP-OCRv3",
            cpu_threads=1,
            use_textline_orientation=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            text_det_limit_side_len=2000,
            text_det_unclip_ratio=1.4,
            text_det_limit_type="max",
            text_det_thresh=0.3,
            text_det_box_thresh=0.5,
            text_rec_score_thresh=0.0,
            enable_mkldnn=False,
        )
        self._predict_lock = threading.Lock()

    def extract_page(self, file_source: str, page_idx: int, **kwargs) -> PageExtractionResult:
        resolution = kwargs.get("resolution", 150)

        with pdfplumber.open(file_source) as pdf:
            page = pdf.pages[page_idx]
            im = page.to_image(resolution=resolution, antialias=True).original
            img_np = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

            result = PageExtractionResult(
                page_number=page_idx + 1,
                width=float(im.width),
                height=float(im.height),
                is_ocr=True,
            )

            with self._predict_lock:
                ocr_result = self.ocr.ocr(img_np)

            if ocr_result and ocr_result[0]:
                res = ocr_result[0]
                texts = res.get("rec_texts", [])
                scores = res.get("rec_scores", [])
                polys = res.get("rec_polys", [])
                for text, score, poly in zip(texts, scores, polys):
                    pts = np.array(poly)
                    x0, y0 = np.min(pts, axis=0)
                    x1, y1 = np.max(pts, axis=0)
                    result.elements.append(SpatialTextElement(
                        text=text,
                        x0=float(x0),
                        y0=float(y0),
                        x1=float(x1),
                        y1=float(y1),
                        confidence=float(score) if score is not None else None,
                    ))

            return result
