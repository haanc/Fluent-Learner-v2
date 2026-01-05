
import os
import subprocess
from pathlib import Path

class AudioService:
    def __init__(self, output_dir: str = "media"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_audio(self, video_path: str) -> str:
        """
        Extracts audio from the given video file using ffmpeg.
        Returns the path to the extracted audio file (mp3).
        """
        video_path_obj = Path(video_path)
        if not video_path_obj.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Create output audio path (same name, but .mp3)
        # We put it in the same directory as the video for now
        audio_path = video_path_obj.with_suffix('.mp3')
        
        # If audio already exists, ideally we skip defined by logic, but here strict overwrite or reuse?
        # Let's overwrite to ensure fresh extraction.
        
        # ffmpeg command:
        # -i input
        # -vn (no video)
        # -acodec libmp3lame (mp3 encoder)
        # -q:a 4 (VBR quality 4, approx 160kbps, good balance of size/quality for Whisper)
        # -y (overwrite)
        
        cmd = [
            "ffmpeg",
            "-i", str(video_path_obj),
            "-vn",
            "-acodec", "libmp3lame",
            "-q:a", "4",
            "-y",
            str(audio_path)
        ]
        
        print(f"DEBUG: Running ffmpeg command: {' '.join(cmd)}")
        
        try:
            # Run ffmpeg, capture output for debugging
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # FFmpeg writes progress to stderr usually
            # print(result.stderr) 
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e.stderr}")
            raise RuntimeError(f"FFmpeg failed: {e.stderr}")
            
        if not audio_path.exists():
            raise RuntimeError("FFmpeg completed but audio file missing.")
            
        print(f"DEBUG: Audio extracted to: {audio_path}")
        return str(audio_path)

audio_service = AudioService()
