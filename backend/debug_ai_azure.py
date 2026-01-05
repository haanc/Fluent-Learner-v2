
from ai_service import ai_service
import os

def test_azure_transcription():
    print("Testing Azure OpenAI Integration...")
    
    # Check env vars
    print(f"Endpoint set: {bool(os.getenv('AZURE_OPENAI_ENDPOINT'))}")
    print(f"API Key set: {bool(os.getenv('AZURE_OPENAI_API_KEY'))}")
    print(f"Whisper Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_WHISPER')}")
    
    print("--- Loaded AZURE Env Vars ---")
    for k, v in os.environ.items():
        if k.startswith("AZURE_"):
            # mask key
            val = v[:4] + "..." if len(v) > 4 else v
            print(f"{k}: {val}")
    
    audio_path = "backend/test_audio.mp3"
    try:
        segments = ai_service.transcribe_audio(audio_path)
        print("Success! Segments received:")
        for seg in segments:
            print(seg)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_azure_transcription()
