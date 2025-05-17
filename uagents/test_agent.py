import asyncio
import json
import sys
import aiohttp

# Default to localhost, but allow overriding from command line
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

async def test_health_endpoint():
    """Test the health endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/health") as response:
            print(f"Health check status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Health check response: {json.dumps(data, indent=2)}")
                return True
            return False

async def test_protocols_list():
    """Test the protocols list endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/protocols/list") as response:
            print(f"Protocols list status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Found {data.get('count', 0)} protocols")
                print(f"Protocols: {json.dumps(data.get('protocols', {}), indent=2)}")
                return True
            return False

async def test_protocol_info(protocol_name="solana"):
    """Test the protocol info endpoint."""
    async with aiohttp.ClientSession() as session:
        payload = {"protocol_name": protocol_name}
        async with session.post(
            f"{BASE_URL}/protocol/info", 
            json=payload
        ) as response:
            print(f"Protocol info status for '{protocol_name}': {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Protocol info: {json.dumps(data, indent=2)}")
                return True
            else:
                error = await response.text()
                print(f"Error: {error}")
                return False

async def main():
    """Run all tests."""
    print(f"Testing agent at {BASE_URL}")
    print("-" * 50)
    
    health_ok = await test_health_endpoint()
    print("-" * 50)
    
    if health_ok:
        await test_protocols_list()
        print("-" * 50)
        
        # Test a valid protocol
        await test_protocol_info("solana")
        print("-" * 50)
        
        # Test an invalid protocol
        await test_protocol_info("nonexistent")
    else:
        print("Health check failed, skipping other tests")
    
    print("Testing completed")

if __name__ == "__main__":
    asyncio.run(main()) 