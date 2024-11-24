#!/bin/bash

# Set any environment variables if needed
export PYTHONUNBUFFERED=1

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000