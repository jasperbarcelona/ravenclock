#!/bin/bash
. venv/bin/activate
export DATABASE_URL='sqlite:///local.db'
export PORT=7000
python server.py