#!/bin/sh
set -e
# Start SSH service
service ssh start
# Start the application
exec python /src/src/app.py
