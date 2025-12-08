#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
which python
sudo .venv/bin/python main.py
deactivate
