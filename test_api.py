# test_api.py - Testar a API REST

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    print("=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_propose_memory():
    print("=== Testing Propose Memory ===")
    memory = {
        "principle": "API Test Principle",
        "context": "Testing the REST API",
        "decision": "Accept the test memory",
        "justification": "This is an automated test",
        "confidence": 0.88,
        "tags": ["test", "api"]
    }
    response = requests.post(f"{BASE_URL}/memories/propose", json=memory)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.json()

def test_graph_summary():
    print("=== Testing Graph Summary ===")
    response = requests.get(f"{BASE_URL}/memories/graph")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_influence_query():
    print("=== Testing Influence Query ===")
    query_data = {
        "query": "How should we handle user data privacy?",
        "top_k": 3
    }
    response = requests.post(f"{BASE_URL}/query/influence", json=query_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Strategy: {result['influence_strategy']}")
    print(f"Memories used: {result['memories_used']}")
    print(f"Prompt preview: {result['influenced_prompt'][:200]}...\n")

def test_governance_status():
    print("=== Testing Governance Status ===")
    response = requests.get(f"{BASE_URL}/governance/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("🚀 Testing SEM API\n")
    
    # Primeiro, garantir que a API está a correr
    try:
        test_root()
    except requests.exceptions.ConnectionError:
        print("❌ API não está a correr!")
        print("   Corre primeiro: python api.py")
        exit(1)
    
    test_propose_memory()
    test_graph_summary()
    test_influence_query()
    test_governance_status()
    
    print("✅ All tests completed!")
