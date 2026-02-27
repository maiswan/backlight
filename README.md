## backlight

backlight is a FastAPI-based LED controller for WS281x strips (WS2812B, SK6812, ...) for Raspberry Pi. Tested on the Raspberry Pi 4 and 5, backlight likely has some degree of backward compatibility.

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

### 2a. Install packages

```bash
pip install -r requirements.txt
```

### 2b. Expand SPI buffer (For Pi 5 only)
> [!WARNING]
> This section only necessary if you have a Pi 5 or if you use SPI (instead of PWM) to control the LEDs.

1. Enable the SPI Interface with `sudo raspi-config`
    
    Select _3 Interface Options_, then _I4 SPI_, then _Yes_.

2. Expand the SPI buffer

    Edit `/boot/cmdline` and append `spidev.bufsiz = 65535` to the same line. Reboot.

3. Instruct backlight to use SPI

    Edit `config.json` and set `mode` (under `leds` and `transport`) to `spi`

4. Connect the LED data line to the SPI pin (i.e., GPIO10)


### 3. Final touches
Modify `config.json` as needed.

Run (`sudo` as needed).
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
| `GET` | `/api/v4/commands` | Get the current commands |
| `POST` | `/api/v4/commands` | Create a new command |
| `PUT` | `/api/v4/commands` | Replace all existing commands with the payload |
| `DELETE` | `/api/v4/commands` | Delete all existing commands |
| `GET` | `/api/v4/commands/{id_or_name}` | Retrieve an existing command |
| `PUT` | `/api/v4/commands/{id_or_name}` | Modify an existing command |
| `DELETE` | `/api/v4/commands/{id_or_name}` | Delete an existing command |
| `POST` | `/api/v4/commands/redraw` | Restart the render pipeline |
| `GET` | `/api/v4/config` | Get the current configurations and commands |
| `GET` | `/api/v4/config/stream` | Get the current configurations and commands via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |

Each configuration item has a GET and a PUT endpoint. When sending a PUT request, encapsulate the value in a JSON object:

```
PUT /api/v4/renderer/framerate/active
```
```json
{
    "value": 60
}
```

Updating the `port` value will require restarting backlight.
