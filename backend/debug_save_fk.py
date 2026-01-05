
import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_fk_constraint():
    print("Step 1: Create Dummy Media...")
    media_id = str(uuid.uuid4())
    media_payload = {
        "id": media_id,
        "title": "FK Test Media",
        "source_url": "http://test.com/fk",
        "file_path": "test.mp4",
        "duration": 10.0,
        "language": "en",
        "status": "ready"
    }
    
    try:
        res = requests.post(f"{BASE_URL}/media", json=media_payload)
        print(f"Create Media Status: {res.status_code}")
        if res.status_code != 200:
            print(res.text)
            return
            
        print("Step 2: Save Word linked to Media...")
        word_payload = {
            "word": "LinkedWord",
            "context_sentence": "Linked context.",
            "translation": "Linked",
            "media_id": media_id,
            "media_time": 5.0
        }
        res = requests.post(f"{BASE_URL}/vocab", json=word_payload)
        print(f"Save Word Status: {res.status_code}")
        print(f"Response: {res.text}")
        
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_fk_constraint()
