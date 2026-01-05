
import requests

def verify_save():
    print("Attempting to save word locally...")
    try:
        res = requests.post("http://127.0.0.1:8000/vocab", json={
            "word": "LocalDebug",
            "context_sentence": "Local context",
            "translation": "Debug"
        })
        print(f"Status: {res.status_code}")
        print(f"Body: {res.text}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    verify_save()
