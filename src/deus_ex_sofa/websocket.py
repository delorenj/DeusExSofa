"""Pure Python WebSocket client (RFC 6455) with SSL/TLS support."""

import socket
import ssl
import json
import base64
import struct
import os
from typing import Optional, Dict, Any


class SimpleWebSocket:
    """Minimal WebSocket client using only standard library."""

    def __init__(self, host: str, port: int, path: str, timeout: int = 10):
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None
        self.ssl_sock: Optional[ssl.SSLSocket] = None

    def connect(self) -> None:
        """Establish WebSocket connection with TLS."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.ssl_sock = context.wrap_socket(self.sock, server_hostname=self.host)
        self.ssl_sock.connect((self.host, self.port))

        # WebSocket handshake
        key = base64.b64encode(os.urandom(16)).decode("utf-8")
        request = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self.ssl_sock.write(request.encode("utf-8"))

        response = self.ssl_sock.read(4096).decode("utf-8", errors="ignore")
        if "101 Switching Protocols" not in response:
            raise ConnectionError(f"WebSocket handshake failed: {response}")

    def send_json(self, data: Dict[str, Any]) -> None:
        """Send JSON payload as WebSocket frame."""
        payload = json.dumps(data).encode("utf-8")
        self._send_frame(payload)

    def receive_json(self) -> Optional[Dict[str, Any]]:
        """Receive and decode JSON payload from WebSocket frame."""
        payload = self._recv_frame()
        if payload:
            try:
                payload_str = payload.decode("utf-8").strip()
                if payload_str:
                    return json.loads(payload_str)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return None

    def _send_frame(self, payload: bytes, opcode: int = 0x1) -> None:
        """Send WebSocket frame with masking (RFC 6455)."""
        header = bytearray()
        b1 = 0x80 | (opcode & 0x0F)
        header.append(b1)

        length = len(payload)
        if length <= 125:
            b2 = 0x80 | length
            header.append(b2)
        elif length <= 65535:
            b2 = 0x80 | 126
            header.append(b2)
            header.extend(struct.pack("!H", length))
        else:
            b2 = 0x80 | 127
            header.append(b2)
            header.extend(struct.pack("!Q", length))

        masking_key = os.urandom(4)
        header.extend(masking_key)

        masked_payload = bytearray(length)
        for i in range(length):
            masked_payload[i] = payload[i] ^ masking_key[i % 4]

        self.ssl_sock.write(header + masked_payload)

    def _recv_frame(self) -> Optional[bytes]:
        """Receive WebSocket frame and unmask payload."""
        try:
            head = self.ssl_sock.read(2)
        except (socket.timeout, OSError):
            return None

        if not head or len(head) < 2:
            return None

        b1, b2 = head[0], head[1]
        length = b2 & 0x7F

        if length == 126:
            data = self.ssl_sock.read(2)
            if len(data) < 2:
                return None
            length = struct.unpack("!H", data)[0]
        elif length == 127:
            data = self.ssl_sock.read(8)
            if len(data) < 8:
                return None
            length = struct.unpack("!Q", data)[0]

        payload = b""
        while len(payload) < length:
            chunk = self.ssl_sock.read(length - len(payload))
            if not chunk:
                break
            payload += chunk

        return payload

    def close(self) -> None:
        """Close WebSocket connection."""
        if self.ssl_sock:
            self.ssl_sock.close()
