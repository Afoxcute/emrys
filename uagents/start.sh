#!/bin/bash

# Default port if not specified in environment
export PORT="${PORT:-8080}"

# Default Railway URL if not specified
export RAILWAY_URL="${RAILWAY_URL:-emrys-production.up.railway.app}"

# Print startup information with better formatting
echo "-------------------------------------------------------------------------"
echo "                  Starting Emrys uAgent Server                          "
echo "-------------------------------------------------------------------------"
echo "➡️  Server Port: $PORT"
echo "➡️  Endpoint URL: $RAILWAY_URL"
echo "-------------------------------------------------------------------------"
echo "💡 Note: The uAgent serves as a messaging system, not an HTTP API server."
echo "   The frontend uses static data to avoid connection issues."
echo "-------------------------------------------------------------------------"

# Set proper permissions for Python files if needed
if [ ! -x "agent.py" ]; then
    echo "Setting executable permissions on agent.py"
    chmod +x agent.py
fi

# Start the agent
echo "🚀 Starting agent..."
python agent.py 