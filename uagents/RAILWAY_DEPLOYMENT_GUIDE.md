# Deploying the Emrys FAQ uAgent to Railway

This guide provides step-by-step instructions for deploying the Emrys FAQ uAgent to Railway, including how to resolve common issues.

## Prerequisites

- A GitHub account
- A Railway account (sign up at [railway.app](https://railway.app))
- Your code pushed to a GitHub repository

## Deployment Steps

### 1. Prepare Your Repository

Make sure your code is pushed to a GitHub repository that Railway can access.

### 2. Create a New Railway Project

1. Log in to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. If prompted for a subdirectory, enter `uagents` since our agent code is in this directory

### 3. Configure Environment Variables

After creating the project, you'll need to set up environment variables:

1. Go to the "Variables" tab in your Railway project
2. Add the following variables:
   - `AGENT_SEED`: A random secure string (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `LOG_LEVEL`: Set to "INFO" (or "DEBUG" for more verbose logging)
   - `PORT`: Railway sets this automatically, no need to configure

3. After the first deployment, you'll need to update:
   - `BASE_URL`: Set to your actual Railway app URL (e.g., `https://your-app-name.up.railway.app`)

### 4. Monitor the Deployment

1. Go to the "Deployments" tab to monitor the deployment process
2. Check the logs for any errors

### 5. Update Frontend Configuration

After your uAgent is successfully deployed:

1. Update your frontend application's `.env` file:
   ```
   NEXT_PUBLIC_UAGENT_URL=https://your-app-name.up.railway.app
   ```

2. Rebuild and deploy your frontend application

## Testing Your Deployed uAgent

Test your deployed agent with these endpoints:

1. Health check: `GET https://your-app-name.up.railway.app/health`
2. List protocols: `GET https://your-app-name.up.railway.app/protocols/list`
3. Chat endpoint: 
   ```
   POST https://your-app-name.up.railway.app/chat/question
   Content-Type: application/json
   
   {
     "question": "What is Emrys?"
   }
   ```

## Troubleshooting Common Issues

### "Agent has no attribute 'middleware'" Error

If you see this error:
```
AttributeError: 'Agent' object has no attribute 'middleware'
```

**Solution**: The uAgents library doesn't support custom middleware. Instead, use FastAPI's CORS middleware as shown in the railway_agent.py file.

### CORS Issues

If your frontend cannot communicate with the API due to CORS issues:

**Solution**: Ensure CORS middleware is correctly configured in the FastAPI app:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Agent Not Starting Properly

If the agent isn't starting properly:

**Solution**: Use uvicorn directly to run the FastAPI app instead of agent.run():

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
```

### Railway URL Configuration Issues

**Problem**: Your agent's `BASE_URL` is incorrectly configured.

**Solution**: After the first deployment, get your Railway URL from the dashboard and update the `BASE_URL` environment variable.

## Verifying Success

Your deployment is successful when:

1. The health endpoint returns `{"status": "healthy", ...}`
2. The protocols list endpoint returns a list of available protocols
3. The chat endpoint returns coherent responses to questions

## Updating Your Deployment

To update your deployed agent:

1. Push changes to your GitHub repository
2. Railway will automatically detect the changes and redeploy
3. Check the logs to ensure the deployment was successful 