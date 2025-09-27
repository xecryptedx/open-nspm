from __future__ import annotations

from typing import Any, Dict

from .. import Response


class HTMLResponse(Response):
    def __init__(self, *, content: str, status_code: int = 200, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status_code=status_code, content=content, media_type="text/html", headers=headers or {"content-type": "text/html"}, parsed_body=content)
