#!/bin/bash

# Default port if not specified in environment
export PORT="${PORT:-8080}"

# Print information
echo "Starting Emrys uAgent on port $PORT"

# Start the agent
python agent.py 