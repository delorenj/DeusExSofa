# Migration Guide: tv.py → deus-ex-sofa Package

## What Changed

The standalone `tv.py` script has been refactored into a proper Python package installable via `uv tool install`.

### Architecture Improvements

**Before:**
- Single monolithic script (tv.py:1-237)
- Hardcoded configuration
- Manual sys.argv parsing
- No installation mechanism

**After:**
- Modular package structure with clear separation of concerns
- Environment variable configuration support
- argparse-based CLI with help system
- Installable via `uv tool install`
- XDG-compliant token storage (with backward compatibility)

### Package Structure

```
src/deus_ex_sofa/
├── __init__.py      # Package metadata
├── cli.py           # CLI interface (entry point)
├── client.py        # Samsung TV client abstraction
├── websocket.py     # WebSocket transport layer
├── config.py        # Configuration management
└── constants.py     # Key mappings and defaults
```

## Installation

### New Method (Recommended)

```bash
# Install globally via uv
uv tool install /home/delorenj/code/DeusExSofa

# Or from git (when published)
uv tool install git+https://github.com/delorenj/deus-ex-sofa
```

### Legacy Method (Still Works)

The original `tv.py` script remains functional and untouched.

## Usage Comparison

### Before
```bash
./tv.py vol_up
./tv.py mute 192.168.1.15
```

### After
```bash
# Both commands are available
deus-ex-sofa vol_up
tv mute 192.168.1.15

# New features
tv --list-keys
tv --version
tv --help
```

## Configuration

### Environment Variables (New)

```bash
# Set default TV IP
export SAMSUNG_TV_IP="192.168.1.15"

# Override port (default: 8002)
export SAMSUNG_TV_PORT="8003"

# Custom app name (default: GeminiController)
export SAMSUNG_TV_APP_NAME="MyRemote"

# Custom token file location
export SAMSUNG_TV_TOKEN_FILE="/path/to/token"
```

### Token Storage

**Legacy Location (still supported):**
```
~/.samsung_tv_token
```

**New XDG-Compliant Location:**
```
~/.config/deus-ex-sofa/token
```

The package automatically detects and uses the legacy location if it exists, ensuring backward compatibility.

## Testing Checklist

- [x] Package installs via `uv tool install`
- [x] Both `deus-ex-sofa` and `tv` commands work
- [x] `--version` flag displays version
- [x] `--list-keys` shows all available keys
- [x] `--help` displays usage information
- [x] Zero runtime dependencies (pure stdlib)
- [ ] First-run authentication flow (requires TV)
- [ ] Subsequent commands work with cached token (requires TV)
- [ ] All key commands function correctly (requires TV)

## Rollback Strategy

If issues arise, the original `tv.py` script is preserved and functional:

```bash
./tv.py vol_up  # Still works
```

To completely remove the package:

```bash
uv tool uninstall deus-ex-sofa
```

## Next Steps

1. Test against actual TV to verify protocol compatibility
2. Update README.md with new installation instructions
3. Consider adding to PyPI for global distribution
4. Optional: Add mise task for local development workflow
