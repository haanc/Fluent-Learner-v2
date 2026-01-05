import subprocess
import sys

url = "https://www.youtube.com/watch?v=2V9VjbcjQuw"

print(f"Testing resolution for: {url}")

try:
    # Command: yt-dlp -g -f "best[ext=mp4][protocol^=http]/best[protocol^=http]" <url>
    cmd = ["yt-dlp", "-g", "-f", "best[ext=mp4][protocol^=http]/best[protocol^=http]", url]
    
    print(f"Running command: {' '.join(cmd)}")
    process = subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    print("STDOUT:", process.stdout)
    print("STDERR:", process.stderr)
    
    candidate = process.stdout.strip().split('\n')[0]
    print(f"Candidate URL: {candidate}")
    
    if candidate.startswith("http"):
        print("SUCCESS: Got a valid http link.")
    else:
        print("FAILURE: Did not get http link.")

except subprocess.CalledProcessError as e:
    print(f"CalledProcessError: {e}")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
except Exception as e:
    print(f"Exception: {e}")
