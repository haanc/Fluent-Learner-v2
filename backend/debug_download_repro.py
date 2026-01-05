
from media_service import media_service
import time

url = "https://www.youtube.com/watch?v=2V9VjbcjQuw"

def test_fetch():
    print(f"Testing fetch for {url}...")
    start = time.time()
    try:
        meta = media_service.fetch_metadata(url)
        print(f"Success! Title: {meta.get('title')}")
        print(f"Duration: {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_fetch()
