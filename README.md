## backlight

backlight is a FastAPI-based LED controller for WS281x strips (WS2812B, SK6812, ...) for Raspberry Pi. backlight works on Raspberry Pi 4 and 5, but likely has some degree of backward compatibility.

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
sudo apt-get install python3-dev # install globally
python -m venv .venv
source .venv/bin/activate
```

### 2a. Install packages (PWM) (NOT for Pi 5)
> [!WARNING]
> If you have a Pi 5, skip directly to step 2b instead.

```bash
pip install -r requirements.txt
```

### 2b. Install packages (SPI) (For Pi 5)
> [!WARNING]
> This section is recommended for the Pi 5 only.

> [!IMPORTANT]
> With SPI, backlight can only address 168 RGB LEDs (≈ 126 RGBW LEDs) because of the underlying SPI driver. [The issue is tracked here](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel_SPI/issues/37). 

```bash
# https://gordonlesti.com/light-up-ws2811-leds-with-a-raspberry-pi-5-via-spi/
sudo raspi-config
```
Select _3 Interface Options_, then _I4 SPI_, then _Yes_.

```bash
# https://abyz.me.uk/lg/download.html
sudo apt install swig
sudo apt install python-setuptools python3-setuptools
wget http://abyz.me.uk/lg/lg.zip
unzip lg.zip
cd lg
make
sudo make install
cd ..
pip install -r requirements-pi-5.txt
```

On a Pi 5, the LED data line must be connected to a SPI pin (e.g., GPIO10). In `config.json`, set `spi_enabled` to `true`.

### 3. Final touches
Modify `config.json` as needed.

Run (`sudo` as needed).
```bash
chmod 755 backlight.sh 
./backlight.sh
```

## Configurations

backlight will read and use the first available configuration file from `config.dev.json`, `config.prod.json`, and `config.json`. When exiting, backlight saves the latest configurations and LED commands.

backlight also offers remote control through a HTTP API. The routes are as follows:

| Method | Route | Behavior |
|--------|-------|----------|
| `GET` | `/dashboard` | Dashboard and controller &mdash; requires [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard) |
| `GET` | `/api/v3/commands` | Get the current commands |
| `POST` | `/api/v3/commands` | Create a new command |
| `PUT` | `/api/v3/commands` | Replace all existing commands with the payload |
| `DELETE` | `/api/v3/commands` | Delete all existing commands |
| `GET` | `/api/v3/commands/{id_or_name}` | Retrieve an existing command |
| `PUT` | `/api/v3/commands/{id_or_name}` | Modify an existing command |
| `DELETE` | `/api/v3/commands/{id_or_name}` | Delete an existing command |
| `POST` | `/api/v3/commands/redraw` | Restart the render pipeline |
| `GET` | `/api/v3/config` | Get the current configurations and commands |
| `GET` | `/api/v3/config/stream` | Get the current configurations and commands via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |

There are two endpoints for each of `port`, `led_count`, `pixel_order`, `spi_enabled`, `pwm_pin` and `fps`, `fps_static`.

    GET /api/v3/config/{x}
    PUT /api/v3/config/{x}

When sending a PUT request, encapsulate the value in a JSON object:

```
PUT /api/v3/config/fps
```
```json
{
    "value": 60
}
```

Updating the `port` value will require restarting backlight.
