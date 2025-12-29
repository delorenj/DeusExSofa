# Deus Ex Sofa 🛋️⚡

> "Any sufficiently advanced technology is indistinguishable from magic." — Arthur C. Clarke
> 
> "Any sufficiently deep pile of blankets is indistinguishable from a black hole." — Me, at 2 AM.

**Deus Ex Sofa** (God from the Couch) is a zero-dependency Python script manifested from the sheer, unadulterated rage of losing the physical Samsung remote in the bedsheets *again*. 

We live in an era of LLMs, neural interfaces, and Mars rovers. I refuse to let my media consumption be held hostage by a piece of plastic that has glitched into the 4th dimension between my duvet and the mattress.

## The Vibe

This is not just a remote. It is a declaration of independence from physical matter. By running this script, you are not "changing the channel"; you are reaching into the ether and bending the machine to your will via raw TCP sockets.

## Features (The Flex)

* **Zero Dependencies:** No `pip install websocket-client`. No bloat. I hand-rolled the RFC 6455 WebSocket frame masking and handshake handling using standard `socket` and `ssl` libraries because `pip` is for people who have patience, and I have none.
* **Auto-Auth:** Handles the Samsung Tizen token exchange automatically. It remembers the token so you don't have to get up to hit "Allow" more than once.
* **Latent Rage Optimization:** The code is optimized for the specific velocity at which a developer wants to mute a commercial.

## Setup

### The Enlightened Path (Recommended)

Install as a proper CLI tool using `uv`:

1.  **Clone this temple of laziness:**
    ```bash
    git clone https://github.com/delorenj/deus-ex-sofa.git
    cd deus-ex-sofa
    ```

2.  **Ascend to package nirvana:**
    ```bash
    uv tool install .
    ```

3.  **Configure your target:**
    Set your TV's IP address via environment variable:
    ```bash
    export SAMSUNG_TV_IP="192.168.1.14"
    # Add to ~/.zshrc or ~/.bashrc for persistence
    ```
    Find your TV's IP under Settings > General > Network > Network Status

4.  **The First Handshake:**
    Run a command. Your TV will ask for permission.
    ```bash
    tv vol_up
    ```
    *Look at your TV. Use the physical remote (one last time, I'm sorry) to select "Allow".*

### The Old Ways (Legacy Script)

For those who prefer the direct approach:

1.  **Clone and configure:**
    ```bash
    git clone https://github.com/delorenj/deus-ex-sofa.git
    cd deus-ex-sofa
    ```

2.  **Set your target:**
    Open `tv.py` and edit the `TV_IP` variable.
    ```python
    TV_IP = "192.168.1.14"
    ```

3.  **Grant Execution Rights:**
    ```bash
    chmod +x tv.py
    ```

4.  **Run directly:**
    ```bash
    ./tv.py vol_up
    ```

## Usage

You are now a wizard. Cast spells from your terminal:

```bash
tv power         # Toggle existence
tv vol_up        # More sound
tv vol_down      # Less sound
tv mute          # Silence
tv source        # Switch inputs
tv tools         # The settings menu
```

### Advanced Incantations

```bash
tv --list-keys                    # See all available spells
tv --version                      # Display version
tv --help                         # Summon the help scroll
tv power 192.168.1.15             # Override IP for this invocation
```

### Legacy Script Usage

If using the standalone script:

```bash
./tv.py power      # Toggle existence
./tv.py vol_up     # More sound
```

Or add an alias to `.zshrc` or `.bashrc`:

```bash
alias tv="~/path/to/deus-ex-sofa/tv.py"
```

## Configuration

### Environment Variables

Customize behavior without editing code:

```bash
# TV connection
export SAMSUNG_TV_IP="192.168.1.14"       # Default TV IP
export SAMSUNG_TV_PORT="8002"             # Default: 8002
export SAMSUNG_TV_APP_NAME="MyRemote"     # Default: GeminiController

# Token storage
export SAMSUNG_TV_TOKEN_FILE="/custom/path/token"  # Custom token location
```

Add these to `~/.zshrc` or `~/.bashrc` for persistence.

### Token Storage

The authentication token is stored at:
- **Package:** `~/.config/deus-ex-sofa/token` (XDG-compliant)
- **Legacy:** `~/.samsung_tv_token` (still supported)

The package automatically detects and uses the legacy location if it exists.

## Troubleshooting

* **"It didn't work":** Is your TV on? Is your computer on the same WiFi? Did you set `SAMSUNG_TV_IP`?
* **"The TV keeps asking for permission":** Delete your token file and try again:
  ```bash
  rm ~/.config/deus-ex-sofa/token  # Package installation
  # or
  rm ~/.samsung_tv_token            # Legacy script
  ```
* **"Command not found: tv":** Did you run `uv tool install .`? Is `~/.local/bin` in your PATH?
* **"I found the physical remote":** Throw it away. It is weak. It relies on batteries. You rely on *code*.

