#!/usr/bin/env python3
import asyncio
import requests
import json
import sys
import time

# The base URL of the uAgent
AGENT_URL = "http://127.0.0.1:8080"

def send_protocol_request(protocol_name):
    """Send a request to the agent for information about a protocol."""
    print(f"Requesting information about {protocol_name}...")
    
    # Create the message payload
    payload = {
        "sender": "test-client",
        "destination": "emrys-defi-agent",
        "message": {
            "protocol_name": protocol_name
        }
    }
    
    try:
        # Send the request to the agent's submit endpoint
        response = requests.post(
            f"{AGENT_URL}/submit",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Try to parse the response
            resp_data = response.json()
            print(f"Success! Received response for {protocol_name}:")
            if "results" in resp_data:
                print(f"\nRESULTS:\n{resp_data['results']}\n")
            else:
                print(f"\nRAW RESPONSE:\n{json.dumps(resp_data, indent=2)}\n")
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"Error sending request: {e}")
        return False

def main():
    """Test the uAgent with a series of protocol requests."""
    print("=== uAgent Test Script ===")
    
    # List of protocols to test
    protocols_to_test = [
        "SOON SVM",
        "IBC",
        "WALRUS",
        "ZPL UTXO Bridge",
        "SVM",
        "UTXO"
    ]
    
    # Test each protocol
    success_count = 0
    for protocol in protocols_to_test:
        if send_protocol_request(protocol):
            success_count += 1
        time.sleep(1)  # Brief pause between requests
    
    # Print summary
    print("\n=== Test Results ===")
    print(f"Successfully tested {success_count} out of {len(protocols_to_test)} protocols")
    
    if success_count == len(protocols_to_test):
        print("\n✅ All tests passed! The uAgent is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 