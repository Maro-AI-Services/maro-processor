from pydantic import BaseModel, Field
from typing import List, Optional


class SpatialTextElement(BaseModel):
    text: str = Field(..., description="The extracted character string or segment.")
    x0: float = Field(..., description="Leftmost pixel or point coordinate border boundary.")
    y0: float = Field(..., description="Topmost pixel or point coordinate border boundary.")
    x1: float = Field(..., description="Rightmost pixel or point coordinate border boundary.")
    y1: float = Field(..., description="Bottommost pixel or point coordinate border boundary.")
    confidence: Optional[float] = Field(None, description="Model tracking extraction validation score.")


class PageExtractionResult(BaseModel):
    page_number: int
    width: float
    height: float
    is_ocr: bool
    elements: List[SpatialTextElement] = Field(default_factory=list)

    def to_layout_text(self, char_width: float = 8.0, line_height: float = 14.0) -> str:
        if not self.elements:
            return ""

        lines: dict[int, list[SpatialTextElement]] = {}
        for el in self.elements:
            row_key = int(el.y0 // line_height)
            lines.setdefault(row_key, []).append(el)

        compiled_string = []
        for _, row_elements in sorted(lines.items()):
            row_elements.sort(key=lambda item: item.x0)
            current_line = ""
            for el in row_elements:
                target_char_idx = max(0, int(el.x0 // char_width))
                if len(current_line) < target_char_idx:
                    current_line += " " * (target_char_idx - len(current_line))
                current_line += el.text
            compiled_string.append(current_line)

        return "\n".join(compiled_string)
