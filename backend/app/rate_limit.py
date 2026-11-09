"""Простое ограничение частоты запросов в памяти процесса для публичных форм и входа.

Процесс API один, поэтому счётчиков в памяти достаточно; при перезапуске они обнуляются.
"""
import ipaddress
import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import HTTPException, Request, status

_hits: dict[tuple[str, str], deque] = defaultdict(deque)
_lock = Lock()


# Адреса Cloudflare (https://www.cloudflare.com/ips/), как в conf/cloudflare-realip.conf у nginx
CLOUDFLARE_NETWORKS = tuple(
    ipaddress.ip_network(net)
    for net in (
        "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18",
        "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17",
        "162.158.0.0/15", "104.16.0.0/13", "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22",
        "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32", "2405:b500::/32", "2405:8100::/32",
        "2a06:98c0::/29", "2c0f:f248::/32",
    )
)


def _ip(value: str | None) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address((value or "").strip())
    except ValueError:
        return None


def client_ip(request: Request) -> str:
    """Адрес посетителя для счётчиков.

    Заголовкам верим не слепо: X-Real-IP ставит (перезаписывая) nginx на этой же машине, поэтому он учитывается
    только для запроса с loopback; CF-Connecting-IP — только если nginx получил запрос от сети Cloudflare.
    Иначе подменой заголовков можно было бы на каждый запрос назваться новым адресом и обойти лимит входа.
    """
    peer = _ip(request.client.host if request.client else None)
    if peer is None:
        return "unknown"
    if not peer.is_loopback:
        return str(peer)  # API открыт напрямую, без nginx — верим только TCP-адресу
    edge = _ip(request.headers.get("x-real-ip"))
    if edge is None:
        return str(peer)
    if any(edge in net for net in CLOUDFLARE_NETWORKS):
        visitor = _ip(request.headers.get("cf-connecting-ip"))
        if visitor is not None:
            return str(visitor)
    return str(edge)


def rate_limit(scope: str, limit: int, window_seconds: int):
    """Зависимость FastAPI: не больше limit запросов за window_seconds с одного адреса."""

    def dependency(request: Request) -> None:
        key = (scope, client_ip(request))
        now = time.monotonic()
        with _lock:
            hits = _hits[key]
            while hits and now - hits[0] > window_seconds:
                hits.popleft()
            if not hits:
                _hits.pop(key, None)  # не копить пустые ключи разовых посетителей
                hits = _hits[key]
            if len(hits) >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Слишком много запросов. Попробуйте через несколько минут.",
                )
            hits.append(now)

    return dependency
