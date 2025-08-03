## backlight

Backlight is a FastAPI-based LED controller for WS2812B strips. It is designed for Raspberry Pi but should work on other platforms as adjusted.

## Features

* Multiple built-in instructions (colors, brightness, gamma correction, animations...)
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

All configurations are stored in `config.json`. Backlight saves the currently executing LED instructions when it exits and applies them automatically on startup.

Backlight also offers remote control through a HTTP API. The routes are as follows:

| Request | Path | Functionality |
|---------|------|---------------|
| `GET` | `/dashboard` | Dashboard and controller &mdash; requires [maiswan/backlight-dashboard](https://github.com/maiswan/backlight-dashboard) |
| `GET` | `/api/v1/config` | Get the current configurations and instructions |
| `GET` | `/api/v1/config/stream` | Get the current configurations and instructions via [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) |
| `GET` | `/api/v1/instructions` | Get the current instructions |
| `POST` | `/api/v1/instructions` | Create a new instruction |
| `PUT` | `/api/v1/instructions` | Replace all existing instructions with the payload |
| `DELETE` | `/api/v1/instructions` | Delete all existing instructions |
| `PUT` | `/api/v1/instructions/{id}` | Modify an existing instruction |
| `DELETE` | `/api/v1/instructions/{id}` | Delete an existing instruction |
