# Emrys Protocol Info Agent for Railway

This is a uAgent service that provides information about various blockchain protocols and technologies via REST endpoints.

## Deployment on Railway

### Setup

1. Create a Railway account and project.
2. Connect your repository to Railway.
3. Set the following environment variables in Railway:
   - `PORT`: The port your agent will run on (Railway will assign this automatically)
   - `AGENT_SEED`: A secure seed phrase for your agent (optional, defaults provided)
   - `AGENT_ENDPOINT`: The endpoint URL (will be assigned by Railway)

### Available Endpoints

- **GET /health**: Check if the agent is running properly
  ```
  curl https://your-railway-url.railway.app/health
  ```

- **POST /protocol/info**: Get information about a specific blockchain protocol
  ```
  curl -d '{"protocol_name": "solana"}' -H "Content-Type: application/json" -X POST https://your-railway-url.railway.app/protocol/info
  ```

- **GET /protocols/list**: Get a list of all available protocols
  ```
  curl https://your-railway-url.railway.app/protocols/list
  ```

### Example Responses

**Health Check:**
```json
{
  "status": "healthy",
  "timestamp": 1694529821
}
```

**Protocol Info:**
```json
{
  "timestamp": 1694529821,
  "protocol_name": "solana",
  "information": "Solana is a high-performance blockchain supporting builders around the world creating crypto apps that scale today...",
  "agent_address": "agent1q2qavahvzm2yw237g2cq40pe8p590ppysclaffp2dd0gtk9evtxag7c8djd"
}
```

**Protocol List:**
```json
{
  "timestamp": 1694529821,
  "protocols": {
    "solana": "Solana",
    "svm": "SVM",
    "soon": "Soon SVM",
    "walrus": "Walrus",
    "utxo": "UTXO",
    "ibc": "IBC",
    "zpl": "ZPL UTXO Bridge",
    "walletconnect": "WalletConnect Integration",
    "mainnet": "Mainnet Deployment"
  },
  "count": 9
}
```

## Local Development

To run the agent locally:

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```
   python railway_agent.py
   ```

3. The agent will be available at `http://localhost:8000` by default. 