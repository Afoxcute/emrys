FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all agent files
COPY *.py .

# Default environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose the port (Railway will set the actual port)
EXPOSE $PORT

# Health check to verify the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

# Start the agent
CMD python agent.py 