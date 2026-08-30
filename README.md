## backlight

backlight is a FastAPI-based LED controller for WS281x strips (WS2812B, SK6812, ...) for Raspberry Pi.

## Features

* Multiple built-in commands (colors, brightness, gamma correction, animations...)
* Individual LED addressable
* Highly configurable from
    * JSON config file
    * RESTful API
* React frontend at [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard)

## Setup
### 1. Initialize a Python virtual environment
```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
```

### 2. Install packages
 
#### 2a. To use PWM and _not_ a Pi 5 (recommended):

```bash
pip install -r requirements.txt
```

#### 2b. To use PWM and a Pi 5:

WIP.

#### 2c. To use SPI (don't):

```bash
pip install -r requirements-spi.txt
```

1. Enable SPI interface
```bash
sudo raspi-config
# Select 3 Interface Options > I4 SPI > Yes
```

2. Expand SPI buffer: edit `/boot/firmware/cmdline.txt` and append the following setting to the end of the line

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
        ...
    }
    ...
}
```

5. Connect the LED data line to the SPI MOSI data pin (i.e., GPIO pin 10, aka physical pin 19)


### 3. Final touches
Modify `config.json` as needed.

```bash
chmod 755 backlight.sh 
./backlight.sh
```

## Configurations

backlight reads and uses the first available configuration file from `config.dev.json`, `config.prod.json`, and `config.json`. When exiting, backlight saves the latest configurations and LED commands.

backlight also offers remote control through a HTTP API. The routes are as follows:

| Method | Route | Behavior |
|--------|-------|----------|
| `GET` | `/dashboard` | Dashboard and controller &mdash; requires [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard) |
| `GET` | `/api/v4/commands` | Retrieve the current commands |
| `POST` | `/api/v4/commands` | Create a new command |
| `PUT` | `/api/v4/commands` | Replace all existing commands |
| `DELETE` | `/api/v4/commands` | Delete all existing commands |
| `GET` | `/api/v4/commands/{id_or_name}` | Retrieve an existing command |
| `PUT` | `/api/v4/commands/{id_or_name}` | Overwrite an existing command |
| `PATCH` | `/api/v4/commands/{id_or_name}` | Change field(s) of an existing command |
| `DELETE` | `/api/v4/commands/{id_or_name}` | Delete an existing command |
| `POST` | `/api/v4/commands/redraw` | Restart the render pipeline |
| `GET` | `/api/v4` | Get the current configurations and commands |
| `GET` | `/api/v4/stream` | Get the current configurations and commands via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |

Each configuration item has a GET and a PUT endpoint. When sending a PUT request, encapsulate the value in a JSON object:

```
PUT /api/v4/renderer/framerate/active
```
```json
{
    "value": 60
}
```

Updating values under `server` requires restarting backlight.
