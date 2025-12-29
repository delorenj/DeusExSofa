"""Samsung TV remote control client."""

import base64
import time
from typing import Optional

from .websocket import SimpleWebSocket
from .config import Config
from .constants import KEYS, AUTH_TIMEOUT


class SamsungTVClient:
    """High-level interface for Samsung TV remote control."""

    def __init__(self, config: Config):
        self.config = config
        self.token: Optional[str] = None

    def send_key(self, key_name: str, tv_ip: Optional[str] = None) -> None:
        """
        Send remote control key command to TV.

        Args:
            key_name: Key identifier from KEYS dictionary
            tv_ip: Override configured TV IP address

        Raises:
            ValueError: If key_name is not recognized
            ConnectionError: If unable to connect to TV
        """
        if key_name not in KEYS:
            raise ValueError(
                f"Unknown key: {key_name}. Available: {', '.join(sorted(KEYS.keys()))}"
            )

        key_code = KEYS[key_name]
        ip = tv_ip or self.config.tv_ip

        # Load cached token
        self.token = self.config.load_token()

        # Build WebSocket path with authentication
        name_b64 = base64.b64encode(self.config.app_name.encode("utf-8")).decode("utf-8")
        path = f"/api/v2/channels/samsung.remote.control?name={name_b64}"
        if self.token:
            path += f"&token={self.token}"

        ws = SimpleWebSocket(ip, self.config.tv_port, path)

        try:
            ws.connect()

            # Handle token exchange if not authenticated
            if not self.token:
                self._authenticate(ws)

            # Send remote control command
            command = {
                "method": "ms.remote.control",
                "params": {
                    "Cmd": "Click",
                    "DataOfCmd": key_code,
                    "Option": "false",
                    "TypeOfRemote": "SendRemoteKey",
                },
            }

            ws.send_json(command)
            time.sleep(0.2)  # Allow command to process

        finally:
            ws.close()

    def _authenticate(self, ws: SimpleWebSocket) -> None:
        """Handle TV pairing and token exchange."""
        print(f"Connecting to {self.config.tv_ip}...")
        print("No cached token found. CHECK YOUR TV and accept the permission prompt within 30 seconds.")

        start_time = time.time()
        while time.time() - start_time < AUTH_TIMEOUT:
            resp = ws.receive_json()
            if resp:
                if "data" in resp and "token" in resp["data"]:
                    self.token = resp["data"]["token"]
                    self.config.save_token(self.token)
                    print(f"Success! Token saved to {self.config.token_file}")
                    return

                if resp.get("event") == "ms.channel.connect":
                    # Connection established, waiting for token
                    pass

            time.sleep(0.1)

        if not self.token:
            print("Warning: Timed out waiting for token.")
            print("If you saw the prompt and accepted, try running the command again.")
            print("If you didn't see a prompt, check TV Settings > General > External Device Manager.")
