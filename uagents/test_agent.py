import asyncio
import json
import sys
import aiohttp

# Replace with the actual URL where your agent is running
BASE_URL = "http://localhost:8000"

async def test_health_endpoint():
    """Test the health endpoint of the agent"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"Health check successful: {data}")
                return True
            else:
                print(f"Health check failed with status: {response.status}")
                return False

async def test_protocols_list():
    """Test the protocols list endpoint of the agent"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/protocols/list") as response:
            if response.status == 200:
                data = await response.json()
                print(f"Protocols list: {json.dumps(data, indent=2)}")
                return True
            else:
                print(f"Failed to get protocols list with status: {response.status}")
                return False

async def test_protocol_info(protocol_name="solana"):
    """Test the protocol info endpoint of the agent"""
    payload = {"protocolName": protocol_name}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/protocol/info", json=payload) as response:
            if response.status == 200:
                data = await response.json()
                print(f"\nProtocol info for '{protocol_name}':")
                print(json.dumps(data, indent=2))
                return True
            else:
                print(f"Failed to get protocol info with status: {response.status}")
                return False

async def test_chat_faq():
    """Test the chat FAQ endpoint of the agent"""
    questions = [
        "What is Emrys?",
        "Which chains are supported?",
        "Tell me about bridge fees",
        "Hello there!",
    ]
    
    async with aiohttp.ClientSession() as session:
        for question in questions:
            payload = {"question": question}
            async with session.post(f"{BASE_URL}/chat/faq", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"\nQuestion: '{question}'")
                    print(f"Answer: '{data['answer']}'")
                    if 'suggested_questions' in data and data['suggested_questions']:
                        print(f"Suggested questions: {data['suggested_questions']}")
                else:
                    print(f"Failed to get chat response with status: {response.status}")
                    return False
    return True

async def main():
    """Run all tests"""
    print("🧪 Testing Railway agent endpoints...")
    
    # Test health endpoint
    health_ok = await test_health_endpoint()
    if not health_ok:
        print("❌ Health check failed, skipping other tests")
        return
    
    # Test protocols list
    await test_protocols_list()
    
    # Test protocol info
    await test_protocol_info("bitcoin")
    await test_protocol_info("ethereum")
    await test_protocol_info("solana")
    
    # Test chat FAQ
    await test_chat_faq()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 