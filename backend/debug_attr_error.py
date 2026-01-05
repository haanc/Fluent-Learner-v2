
import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def test_attr_error():
    print("Testing Save for AttributeError...")
    # Use a random UUID for media_id to ensure we hit the backend logic
    media_id = str(uuid.uuid4())
    
    payload = {
        "word": "AttrErrorTest",
        "context_sentence": "Testing attribute error.",
        "translation": "Test",
        "media_id": media_id,
        "media_time": 10.0
    }
    try:
        res = requests.post(f"{BASE_URL}/vocab", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_attr_error()
