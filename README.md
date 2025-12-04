## backlight

Backlight is a FastAPI-based LED controller for WS2812B strips for Raspberry Pi. This controller targets Pi 4 and 5, but should have some degree of backward compability

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

### 2a. Install packages (PWM) (For everything OTHER than Pi 5)
> [!WARNING]
> If you have a Pi 5, proceed to step 2b instead.

```bash
pip install -r requirements.txt
```

### 2b. Install packages (SPI) (For Pi 5)
> [!WARNING]
> This section is only for the Pi 5. Return to step 2a otherwise.

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

All configurations are inside `config.json`. Backlight saves the currently executing LED commands when it exits and re-applies them automatically on startup.

Backlight also offers remote control through a HTTP API. The routes are as follows:

| Request | Path | Functionality |
|---------|------|---------------|
| `GET` | `/dashboard` | Dashboard and controller &mdash; requires [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard) |
| `GET` | `/api/v2/commands` | Get the current commands |
| `POST` | `/api/v2/commands` | Create a new command |
| `PUT` | `/api/v2/commands` | Replace all existing commands with the payload |
| `DELETE` | `/api/v2/commands` | Delete all existing commands |
| `PUT` | `/api/v2/commands/{id_or_name}` | Modify an existing command |
| `DELETE` | `/api/v2/commands/{id_or_name}` | Delete an existing command |
| `GET` | `/api/v2/config` | Get the current configurations and commands |
| `GET` | `/api/v2/config/stream` | Get the current configurations and commands via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |

There are two endpoints for each of `led_count`, `pixel_order`, `pwm_pin` and `fps`.

    GET /api/v2/config/{x}
    PUT /api/v2/config/{x}

When sending a PUT request, enclose the value in a JSON object:

```
PUT /api/v2/config/fps
```
```json
{
    "value": 60
}
```
