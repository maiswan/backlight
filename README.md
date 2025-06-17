## backlight

Backlight is a FastAPI-based LED controller for WS2812B strips. It is designed for Raspberry Pi but should work on other platforms as adjusted.

## Features

* Multiple built-in instructions (colors, brightness, gamma correction, animations...)
* Individual LED addressable
* Highly configurable from
    * JSON config file
    * RESTful API
* React frontend at [maiswan/backlight-dashboard](https://github.com/maiswan/dashboard)

## Setup
1. Initialize a Python virtual environment
```bash
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

All configurations are stored in `config.json`. Backlight saves the currently executing LED instructions when it exits and applies them automatically on startup.

Backlight also offers remote control through a HTTP API. The routes are as follows:

| Path | Request | Functionality |
|------|---------|---------------|
| `/dash` | `GET` | Dashboard and controller &mdash; requires [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard) |
| `/state` | `GET` | Get the current configurations, instructions, and LED status |
| `/state?stream=1` | `GET` | Get the current configurations and instructions via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |
| `/instructions/` | `GET` | Get the current instructions |
| `/instructions/` | `POST` | Create a new instruction |
| `/instructions/{id}` | `PUT` | Modify an existing instruction |
| `/instructions/{id}` | `DELETE` | Delete an existing instruction |
| `/instructions/all` | `DELETE` | Delete all existing instructions |
| `/instructions/reset` | `POST` | Replace all existing instructions with the payload |
