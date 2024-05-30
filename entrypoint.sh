#!/bin/bash

# Start FastAPI applications
python3 main.py

# Start Nginx
nginx -g 'daemon off;'
