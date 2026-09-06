## backlight

High-level LED controller for WS281x strips (WS2812B, SK6812, ...) for Raspberry Pi.

Points of interest include:

* Multiple built-in commands (colors, brightness, gamma correction, animations...)
* Highly configurable via JSON config file and RESTful API
* Optional frontend at [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard)

## Setup
### 1. Initialize a Python virtual environment
```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
```

### 2. Install packages
 
#### 2a. With PWM and not a Pi 5 (recommended):

```bash
pip install -r requirements-pwm.txt
```

#### 2b. With SPI (don't):

```bash
pip install -r requirements-spi.txt
```

1. Enable SPI interface
```bash
sudo raspi-config
# Select 3 Interface Options > I4 SPI > Yes
```

2. Expand SPI buffer: edit `/boot/firmware/cmdline.txt` and append the following to the end of the line

```
spidev.bufsiz=32768
```

3. Reboot
4. Edit `config.json`

```json
{
    "led": {
        ...
        "transport": {
            "mode": "spi",
            "speed_khz": 640
        }
    },
    ...
}
```

5. Connect the LED data line to the SPI0 MOSI data pin (i.e., GPIO pin 10, aka physical pin 19)


### 3. Final touches

```bash
chmod 755 backlight.sh 
./backlight.sh
```

## Configuration

### JSON file
backlight uses the first available configuration from `config.dev.json`, `config.prod.json`, and `config.json`. When exiting, backlight writes the latest configurations and LED commands back to the file it read from.

### HTTP endpoints

The default port number is 12021.

| Method | Route | Behavior |
|--------|-------|----------|
| `GET` | `/` | Get program version |
| `GET` | `/dashboard` | Controller sample |
| `GET` | `/api/v4` | Get all configuration |
| `GET` | `/api/v4/stream` | Get all configuration as SSE |

Each configuration section (`server`, `leds`, `renderer`) has a `GET` and `PATCH` endpoint.

| Method | Route | Behavior |
|--------|-------|----------|
| `GET` | `/api/v4/...` | Get all configuration items for the section |
| `PATCH` | `/api/v4/...` | Change one or more settings in the section |

Patching values under `server` and `leds` requires restarting backlight.

To interact with the list of commands and the renderer:

<table>
    <thead>
      <tr>
        <th>Method</th>
        <th>Route</th>
        <th>Behavior</th>
      </tr>  
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td rowspan="4"
            ><code>/api/v4/commands</code></td>
            <td>Get all commands</td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td>Replace all commands with request body</td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td>Add a new command</td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td>Delete all commands</td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td rowspan="4"
            ><code>/api/v4/commands/{identifier}</code></td>
            <td>Get a command by UUID or name</td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td>Replace a command with request body</td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td>Change an existing command except the <code>mode</code> property</td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td>Delete a command</td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/v4/renderer/buffer</code></td>
            <td>Get the current renderer buffer</td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/v4/renderer/redraw</code></td>
            <td>Restart the rendering pipeline</td>
        </tr>
    </tbody>
</table>



