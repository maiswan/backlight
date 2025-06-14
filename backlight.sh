#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
sudo .venv/bin/uvicorn main:app --host 0.0.0.0 --port 12021
