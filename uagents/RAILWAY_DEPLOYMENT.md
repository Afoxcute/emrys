# Deploying the Emrys uAgent to Railway

## Overview

This guide walks through the process of deploying the Emrys uAgent service to Railway.

## Prerequisites

- A Railway account
- The Railway CLI (optional)
- Docker installed locally (for testing)

## Deployment Steps

### Option 1: Deploy via GitHub

1. Push your code to a GitHub repository
2. In Railway dashboard, click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository and branch
5. Railway will automatically detect the Dockerfile in the uagents directory
6. Click "Deploy"

### Option 2: Deploy via Railway CLI

1. Install the Railway CLI:
   ```
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```
   railway login
   ```

3. Initialize a new project:
   ```
   railway init
   ```

4. Navigate to the uagents directory:
   ```
   cd uagents
   ```

5. Deploy the service:
   ```
   railway up
   ```

## Environment Variables

The following environment variables are used by the uAgent:

- `PORT`: The port on which the service will run (automatically set by Railway)
- `HOST`: The host for the service (set to 0.0.0.0 for Railway)
- `AGENT_SEED`: (Optional) A seed phrase for the agent to ensure address consistency

## Setting Up Frontend Connection

After deployment, get the URL of your deployed service from the Railway dashboard and update the frontend environment variable:

```
NEXT_PUBLIC_UAGENT_URL=https://your-emrys-uagent-production.up.railway.app
```

## Testing the Deployment

Once deployed, you can test the REST endpoints:

1. Health Check:
   ```
   curl https://your-emrys-uagent-production.up.railway.app/health
   ```

2. Protocol List:
   ```
   curl https://your-emrys-uagent-production.up.railway.app/protocols/list
   ```

3. Protocol Info:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"protocolName":"solana"}' https://your-emrys-uagent-production.up.railway.app/protocol/info
   ```

## Troubleshooting

If you encounter issues with the deployment:

1. Check the Railway logs for errors
2. Verify that all required files are included in the deployment
3. Make sure CORS is properly configured if you're getting cross-origin errors
4. Ensure the health check endpoint (/health) is responding properly 