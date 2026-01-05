
import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_save_invalid_id():
    print("Testing Save with INVALID Media ID (Random UUID)...")
    random_id = str(uuid.uuid4())
    
    payload = {
        "word": "TestInvalidID",
        "context_sentence": "Testing invalid ID.",
        "translation": "Test",
        "media_id": random_id,
        "media_time": 10.0
    }
    try:
        res = requests.post(f"{BASE_URL}/vocab", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_save_invalid_id()
