# backlight

> [!TIP]
> This repository is in its initial stages &mdash; all functionalities are working but setup instructions are barebone (i.e., YMMV, use your own judgement) now.

Backlight is a FastAPI-based LED controller for WS2812B strips. It also comes with a frontend written in React.

Backlight is designed for Raspberry Pi but should work on other platforms as adjusted.

# Installation
1. [Initialize a Python virtual environment](https://docs.python.org/3/library/venv.html)

2. [Install packages](https://core-electronics.com.au/guides/fully-addressable-rgb-raspberry-pi/)
```bash
sudo pip3 install rpi_ws281x
sudo pip3 install adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
```
A `requirements.txt` will be available in the near future.

3. Build the React frontend
```bash
cd dash
npm install
npm build
```
You may want to do this on your computer since the Pi has very limited computing power.

3. Run `backlight.sh`