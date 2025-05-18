# Deploying uAgent to Railway

This guide will walk you through the process of deploying the Emrys FAQ uAgent to Railway.

## Prerequisites

- A GitHub account
- A Railway account (sign up at [https://railway.app](https://railway.app))
- Git installed on your local machine

## Steps to Deploy

### 1. Prepare your Repository

Make sure your uAgent code is pushed to a GitHub repository. Railway can deploy directly from GitHub.

### 2. Set Up Railway Project

1. Log in to Railway using your GitHub account
2. Click on "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. If prompted for the subdirectory, enter `uagents` since our agent code is in this directory

### 3. Configure Environment Variables

After creating the project, go to the "Variables" tab and add the following environment variables:

- `AGENT_SEED`: A random string to seed the agent (keep this secure)
- `PORT`: This will be automatically set by Railway, so you don't need to configure it
- `BASE_URL`: The URL of your deployed application (you'll set this after the first deployment)

### 4. Initial Deployment

1. Railway will automatically start deploying your application after you've configured it
2. Wait for the deployment to complete
3. Once deployed, you'll get a URL for your application (like `https://your-protocol-agent-production.up.railway.app`)

### 5. Update BASE_URL

1. Go back to the "Variables" tab
2. Add/update the `BASE_URL` variable with your full application URL (e.g., `https://your-protocol-agent-production.up.railway.app`)
3. This will trigger a redeployment

### 6. Test Your Deployment

Once redeployed, test your agent with the following endpoints:

- Health check: `GET https://your-protocol-agent-production.up.railway.app/health`
- Protocol list: `GET https://your-protocol-agent-production.up.railway.app/protocols/list`
- Chat endpoint: `POST https://your-protocol-agent-production.up.railway.app/chat/question` with JSON body `{"question": "What is Emrys?"}`

### 7. Update Frontend Configuration

After confirming that your agent is working correctly, update your frontend application's environment variables:

1. Set `NEXT_PUBLIC_UAGENT_URL` to your Railway app URL in your frontend environment

## Troubleshooting

If you encounter issues with your deployment:

1. Check the Railway logs by clicking on your deployment and selecting the "Logs" tab
2. Make sure all required environment variables are set correctly
3. Verify that your code works locally before deploying
4. If you see CORS issues, ensure the CORS middleware is properly configured

## Maintenance

To update your deployed agent:

1. Push changes to your GitHub repository
2. Railway will automatically detect the changes and redeploy
3. Monitor the deployment logs to ensure everything is working as expected

## Resources

- [Railway Documentation](https://docs.railway.app/)
- [uAgents Documentation](https://docs.fetch.ai/uAgents/) 