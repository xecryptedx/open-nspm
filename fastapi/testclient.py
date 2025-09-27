from __future__ import annotations

from typing import Any, Dict, Optional

from . import FastAPI, Request, Response, UploadFile, parse_request


class TestClient:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def __enter__(self) -> "TestClient":
        self.app.startup()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, tuple[str, bytes, str]]] = None,
    ) -> Response:
        actual_path, query_params = parse_request(path)
        request = Request(
            method=method,
            path=actual_path,
            headers={k.lower(): v for k, v in (headers or {}).items()},
            query_params=query_params,
            json_body=json,
            form_data=data or {},
            files=self._prepare_files(files or {}),
        )
        return self.app.handle_request(request)

    def get(self, path: str, *, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Response:
        if params:
            query = "&".join(f"{key}={value}" for key, value in params.items())
            path = f"{path}?{query}"
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, tuple[str, Any, str]]] = None,
    ) -> Response:
        file_payload: Dict[str, tuple[str, bytes, str]] = {}
        if files:
            for key, value in files.items():
                filename, content, content_type = value
                if hasattr(content, "read"):
                    file_payload[key] = (filename, content.read(), content_type)
                else:
                    file_payload[key] = (filename, content, content_type)
        return self.request("POST", path, headers=headers, json=json, data=data, files=file_payload)

    def _prepare_files(self, files: Dict[str, tuple[str, bytes, str]]) -> Dict[str, UploadFile]:
        prepared: Dict[str, UploadFile] = {}
        for key, (filename, content, content_type) in files.items():
            if isinstance(content, str):
                content_bytes = content.encode()
            else:
                content_bytes = content
            prepared[key] = UploadFile(filename=filename, content=content_bytes, content_type=content_type)
        return prepared
