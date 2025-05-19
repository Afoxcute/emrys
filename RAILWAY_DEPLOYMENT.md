# Deploying Emrys FAQ Chat with uAgent on Railway

This guide explains how to deploy the Emrys FAQ Chat application, which consists of two parts:
1. uAgent backend service - A Python-based uAgent service that provides AI-powered responses
2. Next.js frontend - The user interface for the chat application

## Prerequisites

- A [Railway](https://railway.app/) account
- Git repository with the Emrys codebase
- Basic knowledge of Node.js and Python

## Part 1: Deploying the uAgent Backend Service

### Step 1: Set Up a New Project in Railway

1. Log in to your Railway account
2. Click "New Project" and select "Deploy from GitHub repo"
3. Connect your GitHub repository if not already connected
4. Select the repository containing your Emrys codebase

### Step 2: Configure the uAgent Service

1. In your new Railway project, click "New Service" → "GitHub Repo"
2. Configure the service with the following settings:
   - Root Directory: `uagents` (the folder containing your agent.py and Dockerfile)
   - Service Name: `emrys-uagent-service`
   - Environment: `Docker`

3. Railway will automatically detect the Dockerfile in the uagents directory

### Step 3: Configure Environment Variables

1. Go to the "Variables" tab of your uAgent service
2. Add the following environment variables:
   - `PORT`: `8000` (or your preferred port)
   - `HOST`: `0.0.0.0`
   - `AGENT_SEED`: `your_secure_random_seed` (use a secure random string)

### Step 4: Deploy the uAgent Service

1. Click "Deploy" to deploy your uAgent service
2. Once deployed, Railway will provide a public URL for your service (e.g., https://emrys-uagent-service.up.railway.app)
3. Save this URL as you'll need it for the frontend configuration

## Part 2: Deploying the Next.js Frontend

### Step 1: Add a New Service for the Frontend

1. In the same Railway project, click "New Service" → "GitHub Repo"
2. Configure the service with the following settings:
   - Root Directory: `/` (root directory of your repository)
   - Service Name: `emrys-frontend`
   - Environment: Select Node.js (Railway should auto-detect this)

### Step 2: Configure Environment Variables for the Frontend

1. Go to the "Variables" tab of your frontend service
2. Add the following environment variables:
   - `NEXT_PUBLIC_UAGENT_URL`: Set this to the URL of your uAgent service (e.g., https://emrys-uagent-service.up.railway.app)

### Step 3: Deploy the Frontend

1. Click "Deploy" to deploy your frontend service
2. Once deployed, Railway will provide a public URL for your frontend

## Part 3: Testing and Verification

### Verify the uAgent Service

1. Visit your uAgent service URL + "/health" (e.g., https://emrys-uagent-service.up.railway.app/health)
2. You should see a JSON response like: `{"status":"healthy","timestamp":1234567890,"agent_name":"emrys_technology_agent"}`

### Verify the Frontend

1. Visit your frontend service URL
2. The FAQ Chat should load and display the initial greeting
3. Try asking a question to verify that it's properly connected to the uAgent service

## Part 4: Troubleshooting

### CORS Issues

If you encounter CORS issues:

1. The frontend is configured to use a proxy API route (`/api/uagent`) to avoid CORS issues
2. Verify that the `NEXT_PUBLIC_UAGENT_URL` is set correctly
3. Check Railway's logs for both services to identify potential errors

### uAgent Connection Issues

If the frontend can't connect to the uAgent:

1. Check that the uAgent service is running by visiting its health endpoint
2. Verify that the environment variables are set correctly
3. Check Railway's logs for any errors in the uAgent service

### Custom Domain (Optional)

To use a custom domain:

1. Go to your Railway project settings
2. Click on "Domains"
3. Add your custom domain and follow the provided DNS instructions

## Security Considerations

1. The uAgent service is currently accessible publicly - consider adding authentication if needed
2. The `AGENT_SEED` should be kept secure as it's used to generate the agent's identity
3. Consider implementing rate limiting on the uAgent service for production use

---

By following this guide, you should now have a fully functional Emrys FAQ Chat application deployed on Railway, with the Next.js frontend properly connected to the uAgent backend service. 