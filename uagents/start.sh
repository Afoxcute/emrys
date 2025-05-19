#!/bin/bash

# Default port if not specified in environment
export PORT="${PORT:-8080}"

# Default Railway URL if not specified
export RAILWAY_URL="${RAILWAY_URL:-emrys-production.up.railway.app}"

# Print startup information
echo "Starting Emrys uAgent on port $PORT"
echo "Using endpoint URL: $RAILWAY_URL"

# Start the agent
python agent.py 