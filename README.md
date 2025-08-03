## backlight

Backlight is a FastAPI-based LED controller for WS2812B strips. It is designed for Raspberry Pi but should work on other platforms as adjusted.

## Features

* Multiple built-in commands (colors, brightness, gamma correction, animations...)
* Individual LED addressable
* Highly configurable from
    * JSON config file
    * RESTful API
* React frontend at [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard)

## Setup
1. Initialize a Python virtual environment
```bash
sudo apt-get install python3-dev # install globally
python -m venv .venv
source .venv/bin/activate
```

2. Install packages
```bash
pip install -r requirements.txt
```

3. Modify `config.json` as needed

4. Run (`sudo` as needed)
```bash
chmod 755 backlight.sh 
./backlight.sh
```

## Configurations

All configurations are stored in `config.json`. Backlight saves the currently executing LED commands when it exits and applies them automatically on startup.

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

There are two endpoints for each of `led_count`, `pixel_order`, `gpio_pin` and `fps`.

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