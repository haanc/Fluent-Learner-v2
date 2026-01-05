import yt_dlp
import os

class MediaService:
    def __init__(self, download_dir="cache"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def fetch_metadata(self, url: str):
        """Fetch video metadata using yt-dlp."""
        ydl_opts = {
            'quiet': True, # Keep it quiet to clean up terminal
            'no_warnings': False,
            # Strictly prefer progressive HTTP/HTTPS mp4. Exclude manifests.
            # 22 = 720p mp4, 18 = 360p mp4 (standard youtube progressive)
            'format': 'best[protocol^=http][protocol!*=m3u8][protocol!*=dash][ext=mp4]/best[ext=mp4]', 
            'nocheckcertificate': True,
            'javascript_runtime': 'node',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                stream_url = info.get('url')
                
                print(f"DEBUG: Selected Format ID: {info.get('format_id')}")
                print(f"DEBUG: Selected Protocol: {info.get('protocol')}")
                print(f"DEBUG: Final Stream URL: {stream_url[:100]}...")
                if not stream_url and 'formats' in info:
                    # Look for the best mp4 format
                    mp4_formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('url')]
                    if mp4_formats:
                        stream_url = mp4_formats[-1]['url']
                
                print(f"DEBUG: Found stream URL for {url}: {'Yes' if stream_url else 'No'}")
                
                return {
                    "title": info.get('title'),
                    "duration": info.get('duration'),
                    "thumbnail": info.get('thumbnail'),
                    "url": stream_url,
                    "original_url": url,
                    "uploader": info.get('uploader'),
                    "webpage_url": info.get('webpage_url')
                }
            except Exception as e:
                print(f"ERROR fetching metadata: {str(e)}")
                raise e

    def download_video(self, url: str):
        """Download video to local cache and return the file path."""
        ydl_opts = {
            'outtmpl': f'{self.download_dir}/%(id)s.%(ext)s',
            'merge_output_format': 'mp4', # Force MP4 container for Electron support
            'force_overwrites': True, # Force re-download to fix bad formats
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Delete potential conflicting files first to be safe
            # (Simplistic approach: we rely on yt-dlp overwrite, but sometimes it helps to accept we might change extension)
            
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # Post-download verification: unique case where merge changes extension
            # If we asked for mp4 merge, the final file on disk is .mp4, but prepare_filename might return .mkv if that was the video stream ext.
            if info.get('requested_downloads'):
                # Use the path from the actually downloaded file info
                file_path = info['requested_downloads'][0]['filepath']
            
            # Ensure we return an absolute path with .mp4 extension if possible
            abs_path = os.path.abspath(file_path)
            
            # Fallback: if path is .mkv but .mp4 exists, use .mp4
            if abs_path.endswith('.mkv') and os.path.exists(abs_path.replace('.mkv', '.mp4')):
                abs_path = abs_path.replace('.mkv', '.mp4')
                
            return abs_path

media_service = MediaService()
