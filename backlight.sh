#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
which .venv/bin/python
sudo .venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 12021
