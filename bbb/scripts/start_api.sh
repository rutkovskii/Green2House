#!/bin/bash

# Export the PYTHONPATH environment variable
export PYTHONPATH=/home/debian/bbb

# Kill all running instances of api.py
pkill -f api.py

# Run the api.py script
/usr/bin/python3 /home/debian/bbb/scripts/api.py
