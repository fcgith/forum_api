#!/bin/bash

while true; do
    echo "[$(date)] Running git pull"
    git pull origin main
    if [ $? -eq 0 ]; then
        echo "[$(date)] Git pull successful"
        # Check if Uvicorn is running and kill it
        pkill -f "uvicorn"
        # Start Uvicorn in the background
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
    else
        echo "[$(date)] Git pull failed"
    fi
    echo "[$(date)] Sleeping for 300 seconds"
    sleep 300
done