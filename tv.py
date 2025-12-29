#!/usr/bin/env python3
import socket
import ssl
import json
import base64
import time
import sys
import struct
import os

# --- Configuration ---
TV_IP = "192.168.1.14"
TV_PORT = 8002
APP_NAME = "GeminiController"
TOKEN_FILE = os.path.expanduser("~/.samsung_tv_token")

# --- Key Mapping ---
KEYS = {
    "power": "KEY_POWER",
    "vol_up": "KEY_VOLUP",
    "vol_down": "KEY_VOLDOWN",
    "mute": "KEY_MUTE",
    "up": "KEY_UP",
    "down": "KEY_DOWN",
    "left": "KEY_LEFT",
    "right": "KEY_RIGHT",
    "enter": "KEY_ENTER",
    "return": "KEY_RETURN",
    "back": "KEY_RETURN",
    "home": "KEY_HOME",
    "menu": "KEY_MENU",
    "source": "KEY_SOURCE",
    "guide": "KEY_GUIDE",
    "tools": "KEY_TOOLS",
    "info": "KEY_INFO",
    "red": "KEY_RED",
    "green": "KEY_GREEN",
    "yellow": "KEY_YELLOW",
    "blue": "KEY_BLUE",
    "pause": "KEY_PAUSE",
    "play": "KEY_PLAY",
    "stop": "KEY_STOP",
}

class SimpleWebSocket:
    def __init__(self, host, port, path, timeout=10):
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.sock = None
        self.ssl_sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.ssl_sock = context.wrap_socket(self.sock, server_hostname=self.host)
        self.ssl_sock.connect((self.host, self.port))

        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        request = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self.ssl_sock.write(request.encode('utf-8'))

        response = self.ssl_sock.read(4096).decode('utf-8', errors='ignore')
        if "101 Switching Protocols" not in response:
            raise Exception(f"WebSocket handshake failed: {response}")

    def send_json(self, data):
        payload = json.dumps(data).encode('utf-8')
        self._send_frame(payload)

    def receive_json(self):
        payload = self._recv_frame()
        if payload:
            try:
                payload_str = payload.decode('utf-8').strip()
                if payload_str:
                    return json.loads(payload_str)
            except:
                pass
        return None

    def _send_frame(self, payload, opcode=0x1):
        header = bytearray()
        b1 = 0x80 | (opcode & 0x0f)
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

    def _recv_frame(self):
        try:
            head = self.ssl_sock.read(2)
        except (socket.timeout, Exception):
            return None
            
        if not head or len(head) < 2: return None

        b1, b2 = head[0], head[1]
        length = b2 & 0x7f

        if length == 126:
            data = self.ssl_sock.read(2)
            if len(data) < 2: return None
            length = struct.unpack("!H", data)[0]
        elif length == 127:
            data = self.ssl_sock.read(8)
            if len(data) < 8: return None
            length = struct.unpack("!Q", data)[0]

        payload = b""
        while len(payload) < length:
            chunk = self.ssl_sock.read(length - len(payload))
            if not chunk: break
            payload += chunk
            
        return payload

    def close(self):
        if self.ssl_sock:
            self.ssl_sock.close()

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <key_name> [ip]")
        print("Available keys:", ", ".join(KEYS.keys()))
        sys.exit(1)

    key_cmd = sys.argv[1].lower()
    tv_ip = sys.argv[2] if len(sys.argv) > 2 else TV_IP

    if key_cmd not in KEYS:
        print(f"Unknown key: {key_cmd}")
        sys.exit(1)

    key_code = KEYS[key_cmd]
    
    # 1. Load existing token
    token = ""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                token = f.read().strip()
        except:
            pass

    # 2. Construct URL
    name_b64 = base64.b64encode(APP_NAME.encode('utf-8')).decode('utf-8')
    path = f"/api/v2/channels/samsung.remote.control?name={name_b64}"
    if token:
        path += f"&token={token}"

    ws = SimpleWebSocket(tv_ip, TV_PORT, path)

    try:
        ws.connect()
        
        # 3. Pairing / Token Retrieval
        if not token:
            print(f"Connecting to {tv_ip}...")
            print("No cached token found. Please CHECK YOUR TV and accept the permission prompt within 30 seconds.")
            
            start_time = time.time()
            while time.time() - start_time < 30.0:
                resp = ws.receive_json()
                if resp:
                    # print(f"DEBUG: {resp}") # Uncomment if needed
                    if "data" in resp and "token" in resp["data"]:
                        new_token = resp["data"]["token"]
                        with open(TOKEN_FILE, "w") as f:
                            f.write(new_token)
                        print(f"Success! Token saved to {TOKEN_FILE}")
                        token = new_token
                        break
                    
                    if resp.get("event") == "ms.channel.connect":
                        # We are connected. If we are already allowed, we might not get a token event immediately.
                        # But usually, if we didn't send a token, we should get one back if accepted.
                        pass
                
                time.sleep(0.1)
            
            if not token:
                print("Warning: Timed out waiting for token. If you saw the prompt and accepted, try running the command again.")
                print("If you didn't see a prompt, the TV might already have denied this app. Check TV Settings > General > External Device Manager > Device Connection Manager.")

        # 4. Send Command
        command = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key_code,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        }
        
        ws.send_json(command)
        time.sleep(0.2) 
        ws.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()