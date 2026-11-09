"""Простое ограничение частоты запросов в памяти процесса для публичных форм и входа.

Процесс API один, поэтому счётчиков в памяти достаточно; при перезапуске они обнуляются.
"""
import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import HTTPException, Request, status

_hits: dict[tuple[str, str], deque] = defaultdict(deque)
_lock = Lock()


def client_ip(request: Request) -> str:
    # Сайт стоит за Cloudflare и nginx: настоящий адрес — в их заголовках.
    forwarded = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(scope: str, limit: int, window_seconds: int):
    """Зависимость FastAPI: не больше limit запросов за window_seconds с одного адреса."""

    def dependency(request: Request) -> None:
        key = (scope, client_ip(request))
        now = time.monotonic()
        with _lock:
            hits = _hits[key]
            while hits and now - hits[0] > window_seconds:
                hits.popleft()
            if len(hits) >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Слишком много запросов. Попробуйте через несколько минут.",
                )
            hits.append(now)

    return dependency
