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

1.  **Clone this temple of laziness:**
    ```bash
    git clone [https://github.com/delorenj/deus-ex-sofa.git](https://github.com/delorenj/deus-ex-sofa.git)
    cd deus-ex-sofa
    ```

2.  **Set your target:**
    Open `tv.py` and edit the `TV_IP` variable.
    ```python
    # Find this on your TV under Settings > General > Network > Network Status
    TV_IP = "192.168.1.14" 
    ```

3.  **Grant Execution Rights:**
    ```bash
    chmod +x tv.py
    ```

4.  **The First Handshake:**
    Run a command. Your TV will ask for permission.
    ```bash
    ./tv.py vol_up
    ```
    *Look at your TV. Use the physical remote (one last time, I'm sorry) to select "Allow".*

## Usage

You are now a wizard. Cast spells from your terminal:

```bash
./tv.py power      # Toggle existence
./tv.py vol_up     # More sound
./tv.py vol_down   # Less sound
./tv.py mute       # Silence
./tv.py source     # Switch inputs
./tv.py tools      # The settings menu
```

### Alias for Maximum Efficiency

Do not type `./tv.py` like a peasant. Add this to your `.zshrc` or `.bashrc`:

```bash
alias tv="~/path/to/deus-ex-sofa/tv.py"
```

Now you simply type:
```bash
tv mute
```

## Troubleshooting

* **"It didn't work":** Is your TV on? Is your computer on the same WiFi? Did you edit the IP address in the script?
* **"The TV keeps asking for permission":** Delete `~/.samsung_tv_token` and try again.
* **"I found the physical remote":** Throw it away. It is weak. It relies on batteries. You rely on *code*.

