from __future__ import annotations

import inspect
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import parse_qs, urlparse


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: Any = None):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


@dataclass
class Request:
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    json_body: Any = None
    form_data: Dict[str, Any] = field(default_factory=dict)
    files: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Route:
    path: str
    methods: List[str]
    endpoint: Callable[..., Any]
    dependencies: List[Callable[[Request], Any]] = field(default_factory=list)
    status_code: Optional[int] = None
    response_class: Optional[type] = None

    def full_path(self, prefix: str) -> str:
        if prefix.endswith("/") and self.path.startswith("/"):
            return prefix[:-1] + self.path
        return prefix + self.path


class APIRouter:
    def __init__(self, *, prefix: str = "", tags: Optional[List[str]] = None, dependencies: Optional[List[Callable[[Request], Any]]] = None):
        self.prefix = prefix
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.routes: List[Route] = []

    def add_route(self, path: str, endpoint: Callable[..., Any], *, methods: List[str], status_code: Optional[int] = None, response_class: Optional[type] = None) -> None:
        self.routes.append(
            Route(
                path=path,
                methods=methods,
                endpoint=endpoint,
                dependencies=list(self.dependencies),
                status_code=status_code,
                response_class=response_class,
            )
        )

    def get(self, path: str, *, response_class: Optional[type] = None):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_route(path, func, methods=["GET"], response_class=response_class)
            return func

        return decorator

    def post(self, path: str, *, status_code: Optional[int] = None, response_class: Optional[type] = None):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_route(path, func, methods=["POST"], status_code=status_code, response_class=response_class)
            return func

        return decorator


class FastAPI:
    def __init__(self, *, title: str = "FastAPI", version: str = "0.1.0") -> None:
        self.title = title
        self.version = version
        self._routes: List[tuple[Route, str]] = []
        self._startup_handlers: List[Callable[[], Any]] = []

    def include_router(self, router: APIRouter) -> None:
        for route in router.routes:
            self._routes.append((route, router.prefix))

    def _register_inline_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        methods: List[str],
        response_class: Optional[type] = None,
    ) -> Callable[..., Any]:
        router = APIRouter()
        router.add_route(path, endpoint, methods=methods, response_class=response_class)
        self.include_router(router)
        return endpoint

    def get(self, path: str, *, response_class: Optional[type] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return self._register_inline_route(path, func, methods=["GET"], response_class=response_class)

        return decorator

    def post(self, path: str, *, response_class: Optional[type] = None, status_code: Optional[int] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            router = APIRouter()
            router.add_route(path, func, methods=["POST"], status_code=status_code, response_class=response_class)
            self.include_router(router)
            return func

        return decorator

    def on_event(self, event: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        if event != "startup":
            raise ValueError("Only startup event is supported")

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._startup_handlers.append(func)
            return func

        return decorator

    def startup(self) -> None:
        for handler in self._startup_handlers:
            handler()

    def _match_route(self, method: str, path: str) -> tuple[Route, dict[str, str]]:
        incoming_parts = [part for part in path.strip("/").split("/") if part]
        for route, prefix in self._routes:
            full_path = route.full_path(prefix)
            route_parts = [part for part in full_path.strip("/").split("/") if part]
            if len(route_parts) != len(incoming_parts):
                continue
            if method.upper() not in route.methods:
                continue
            params: dict[str, str] = {}
            matched = True
            for route_part, incoming_part in zip(route_parts, incoming_parts):
                if route_part.startswith("{") and route_part.endswith("}"):
                    params[route_part[1:-1]] = incoming_part
                elif route_part != incoming_part:
                    matched = False
                    break
            if matched:
                return route, params
        raise HTTPException(status_code=404, detail="Not found")

    def handle_request(self, request: Request) -> "Response":
        try:
            route, path_params = self._match_route(request.method, request.path)
            for dependency in route.dependencies:
                dependency(request)
            bound_args = self._build_arguments(route.endpoint, request, path_params)
            result = route.endpoint(**bound_args)
            return self._build_response(result, route)
        except HTTPException as exc:
            body = {"detail": exc.detail}
            return Response(status_code=exc.status_code, content=json.dumps(body), media_type="application/json", parsed_body=body)

    def _convert_type(self, value: str, annotation: Any) -> Any:
        if annotation in {int, "int", "builtins.int"}:
            return int(value)
        if annotation in {float, "float", "builtins.float"}:
            return float(value)
        if annotation in {bool, "bool", "builtins.bool"}:
            return value.lower() in {"true", "1", "yes"}
        return value

    def _build_arguments(self, endpoint: Callable[..., Any], request: Request, path_params: dict[str, str]) -> dict[str, Any]:
        signature = inspect.signature(endpoint)
        arguments: dict[str, Any] = {}
        json_consumed = False
        for name, param in signature.parameters.items():
            if name in path_params:
                arguments[name] = self._convert_type(path_params[name], param.annotation)
                continue
            if name in request.query_params:
                arguments[name] = self._convert_type(request.query_params[name], param.annotation)
                continue
            if name in request.form_data:
                value = request.form_data[name]
                if isinstance(value, str):
                    arguments[name] = self._convert_type(value, param.annotation)
                else:
                    arguments[name] = value
                continue
            if name in request.files:
                arguments[name] = request.files[name]
                continue
            if request.json_body is not None and not json_consumed:
                arguments[name] = request.json_body
                json_consumed = True
                continue
            if param.default is not inspect._empty:
                arguments[name] = param.default
                continue
            raise HTTPException(status_code=400, detail=f"Missing required parameter: {name}")
        return arguments

    def _build_response(self, result: Any, route: Route) -> "Response":
        status_code = route.status_code or 200
        if isinstance(result, Response):
            return result
        from fastapi.responses import HTMLResponse  # local import to avoid circular

        if isinstance(result, HTMLResponse):
            return result
        media_type = "application/json"
        parsed_body = result
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        elif isinstance(result, str):
            content = result
            media_type = "text/plain"
        else:
            content = json.dumps(result, default=str)
        return Response(status_code=status_code, content=content, media_type=media_type, parsed_body=parsed_body)


class Response:
    def __init__(self, *, status_code: int, content: str, media_type: str = "text/plain", headers: Optional[Dict[str, str]] = None, parsed_body: Any = None) -> None:
        self.status_code = status_code
        self.content = content
        self.text = content
        self.media_type = media_type
        self.headers = headers or {"content-type": media_type}
        self._parsed_body = parsed_body

    def json(self) -> Any:
        if isinstance(self._parsed_body, (dict, list)):
            return self._parsed_body
        return json.loads(self.content)


class UploadFile:
    def __init__(self, filename: str, content: bytes, content_type: str | None = None) -> None:
        self.filename = filename
        self._content = content
        self.content_type = content_type or "application/octet-stream"

    def read(self) -> bytes:
        return self._content


def parse_request(path: str) -> tuple[str, Dict[str, str]]:
    parsed = urlparse(path)
    query = {key: values[0] for key, values in parse_qs(parsed.query).items()}
    return parsed.path, query
