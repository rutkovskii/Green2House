#!/bin/bash

# Export the PYTHONPATH environment variable
export PYTHONPATH=/home/debian/bbb

# Kill all running instances of api.py
pkill -f /home/debian/bbb/scripts/api.py


pid=$(sudo lsof -t -i:5000)
if [ -n "$pid" ]; then
    sudo kill "$pid"
    echo "Killed process running on port 5000."
else
    echo "No process running on port 5000."
fi

# Run the api.py script
/usr/bin/python3 /home/debian/bbb/main.py