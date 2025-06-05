# Setting Up the uAgent Integration

To connect the Emrys FAQ chat with your deployed uAgent, follow these steps:

## 1. Create a .env.local file

Create a file named `.env.local` in the root directory of your project with the following content:

```
# uAgent Service URL (replace with your actual Railway URL)
NEXT_PUBLIC_UAGENT_URL=https://your-protocol-agent-production.up.railway.app
```

Replace the URL with your actual Railway deployment URL.

## 2. Restart the development server

If your Next.js development server is already running, restart it to load the new environment variable:

```bash
npm run dev
```

## 3. Verify the connection

Open the application and check the FAQ Chat component. You should see "Connected" in the header if the uAgent is successfully connected.

## 4. Troubleshooting

If you're having issues connecting:

1. Make sure your Railway deployment is running
2. Check that the URL is correct
3. Verify that CORS is properly configured on your uAgent service
4. Check the browser console for any errors

## 5. Testing

Try asking questions about blockchain technologies like:
- "Tell me about Solana"
- "What is SVM?"
- "Explain IBC"

These questions should be routed to your uAgent for answers. 