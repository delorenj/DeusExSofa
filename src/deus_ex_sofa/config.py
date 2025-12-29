"""Configuration management for Samsung TV connection."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Runtime configuration with environment variable support."""

    def __init__(self):
        self.tv_ip = os.getenv("SAMSUNG_TV_IP", "192.168.1.14")
        self.tv_port = int(os.getenv("SAMSUNG_TV_PORT", "8002"))
        self.app_name = os.getenv("SAMSUNG_TV_APP_NAME", "GeminiController")
        self._token_file = os.getenv("SAMSUNG_TV_TOKEN_FILE")

    @property
    def token_file(self) -> Path:
        """Get token file path with XDG-compliant fallback."""
        if self._token_file:
            return Path(self._token_file)

        # Maintain backward compatibility with legacy location
        legacy_path = Path.home() / ".samsung_tv_token"
        if legacy_path.exists():
            return legacy_path

        # XDG-compliant path for new installations
        xdg_config = os.getenv("XDG_CONFIG_HOME")
        if xdg_config:
            config_dir = Path(xdg_config) / "deus-ex-sofa"
        else:
            config_dir = Path.home() / ".config" / "deus-ex-sofa"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "token"

    def load_token(self) -> Optional[str]:
        """Load cached authentication token."""
        token_path = self.token_file
        if token_path.exists():
            try:
                return token_path.read_text().strip()
            except OSError:
                pass
        return None

    def save_token(self, token: str) -> None:
        """Persist authentication token."""
        token_path = self.token_file
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(token)
