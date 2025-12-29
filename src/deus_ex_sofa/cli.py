"""Command-line interface for Deus Ex Sofa."""

import argparse
import sys
from typing import Optional, List

from . import __version__
from .client import SamsungTVClient
from .config import Config
from .constants import KEYS


def create_parser() -> argparse.ArgumentParser:
    """Build argument parser for CLI."""
    parser = argparse.ArgumentParser(
        prog="deus-ex-sofa",
        description="Control Samsung TV from the command line",
        epilog="Example: deus-ex-sofa mute",
    )
    parser.add_argument(
        "key",
        nargs="?",
        help=f"Remote control key to send. Available: {', '.join(sorted(KEYS.keys()))}",
    )
    parser.add_argument(
        "ip",
        nargs="?",
        help="TV IP address (overrides SAMSUNG_TV_IP environment variable)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--list-keys",
        action="store_true",
        help="List all available keys and exit",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.list_keys:
        print("Available keys:")
        for key in sorted(KEYS.keys()):
            print(f"  {key:12} -> {KEYS[key]}")
        return 0

    if not args.key:
        parser.print_help()
        return 1

    config = Config()
    client = SamsungTVClient(config)

    try:
        client.send_key(args.key.lower(), tv_ip=args.ip)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
