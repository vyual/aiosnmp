__all__ = (
    "SnmpV1TrapServer",
    "SnmpV2TrapServer",
)

import asyncio
from typing import Callable, Iterable, Optional, Set, Tuple

from .message import SnmpV2TrapMessage
from .protocols import SnmpTrapV2Protocol, SnmpTrapV1Protocol


async def _default_handler(host: str, port: int, message: SnmpV2TrapMessage) -> None:
    print(f"Got packet from {host}:{port} - {message}")


class SnmpV1TrapServer:
    __slots__ = (
        "host",
        "port",
        "communities",
        "handler",
    )

    def __init__(
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 162,
        handler: Callable = _default_handler,
        communities: Optional[Iterable[str]] = None,
    ) -> None:
        self.host: str = host
        self.port: int = port
        self.communities: Optional[Set[str]] = None
        if communities is not None:
            self.communities = set(communities)
        self.handler: Callable = handler

    async def run(self) -> Tuple[asyncio.BaseTransport, SnmpTrapV1Protocol]:
        loop = asyncio.get_event_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: SnmpTrapV2Protocol(self.communities, self.handler),
            local_addr=(self.host, self.port),
        )
        return transport, protocol


class SnmpV2TrapServer:
    __slots__ = (
        "host",
        "port",
        "communities",
        "handler",
    )

    def __init__(
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 162,
        handler: Callable = _default_handler,
        communities: Optional[Iterable[str]] = None,
    ) -> None:
        self.host: str = host
        self.port: int = port
        self.communities: Optional[Set[str]] = None
        if communities is not None:
            self.communities = set(communities)
        self.handler: Callable = handler

    async def run(self) -> Tuple[asyncio.BaseTransport, SnmpTrapV2Protocol]:
        loop = asyncio.get_event_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: SnmpTrapV2Protocol(self.communities, self.handler),
            local_addr=(self.host, self.port),
        )
        return transport, protocol
