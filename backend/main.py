from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request, Header
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List, Dict, Optional, Any
from uuid import UUID, uuid4
import os
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, get_session
from models import MediaSource, SubtitleSegment, SavedWord
from media_service import media_service
from audio_service import audio_service
from ai_service import ai_service
import uvicorn
import datetime

from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount cache directory for serving local files (important for browser playback)
os.makedirs("cache", exist_ok=True)
app.mount("/static/cache", StaticFiles(directory="cache"), name="cache")

class URLRequest(BaseModel):
    url: str

def get_current_owner(x_owner_id: str = Header(default="guest")) -> str:
    return x_owner_id

from fastapi import Response

@app.get("/media/proxy")
async def proxy_video(url: str, request: Request):
    """Proxy video stream, resolving YouTube URLs and forwarding Range headers."""
    
    print(f"DEBUG: Proxy request for URL: {url[:100]}...", flush=True)
    target_url = url
    
    # 1. Resolve direct stream if needed
    if "youtube.com/watch" in url or "youtu.be" in url or "bilibili.com/video" in url:
        print(f"DEBUG: Attempting to resolve direct stream for {url}", flush=True)
        try:
            import subprocess
            cmd = ["yt-dlp", "-g", "-f", "best[ext=mp4][protocol^=http]/best[protocol^=http]", url]
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)
            candidate = process.stdout.strip().split('\n')[0]
            
            if candidate and candidate.startswith('http'):
                target_url = candidate
                print(f"DEBUG: Resolved Successfully via yt-dlp: {target_url[:50]}...", flush=True)
            else:
                print(f"WARN: yt-dlp ran but returned no http link. Stdout: {process.stdout}", flush=True)
        except Exception as e:
            print(f"WARN: Failed to resolve stream URL: {e}. Falling back to original.", flush=True)

    # 2. Prepare headers for upstream
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if "bilibili.com" in target_url or "billibilli" in target_url:
        headers["Referer"] = "https://www.bilibili.com/"
    # For YouTube/Googlevideo, we DON'T send Referer as it causes 403 on signed links
        
    range_header = request.headers.get("Range")
    if range_header:
        headers["Range"] = range_header
        print(f"DEBUG: Forwarding Client Range: {range_header}", flush=True)

    # 3. Request upstream and forward headers
    client = httpx.AsyncClient()
    try:
        # We need to manually manage the response to get headers BEFORE returning StreamingResponse
        response = await client.request("GET", target_url, headers=headers, follow_redirects=True, timeout=30.0)
        
        # Log upstream headers for debugging
        print(f"DEBUG: Upstream Status: {response.status_code}", flush=True)
        
        # Forward specific headers needed for Range support
        forward_headers = {}
        for h in ["Content-Range", "Content-Length", "Accept-Ranges", "Content-Type"]:
            if h in response.headers:
                forward_headers[h] = response.headers[h]
        
        # Ensure Content-Type is set
        media_type = forward_headers.get("Content-Type", "video/mp4")
        
        # Note: We use response.aiter_bytes() to stream the content
        return StreamingResponse(
            response.aiter_bytes(),
            status_code=response.status_code,
            headers=forward_headers,
            media_type=media_type
        )
    except Exception as e:
        print(f"ERROR: Proxy failed to connect to upstream: {str(e)}", flush=True)
        await client.aclose()
        return StreamingResponse(iter([b""]), status_code=500)

@app.post("/media/fetch-info")
def fetch_media_info(request: URLRequest):
    try:
        return media_service.fetch_metadata(request.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/media/download")
def start_download(request: URLRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session), owner_id: str = Depends(get_current_owner)):
    try:
        # Check for existing video with same URL and SAME OWNER (Deduplication)
        statement = select(MediaSource).where(MediaSource.source_url == request.url).where(MediaSource.owner_id == owner_id)
        existing_media = db.exec(statement).first()

        if existing_media:
            print(f"DEBUG: Found existing media {existing_media.id} for URL {request.url}. Overwriting.")
            # Setup for re-download
            media_id = existing_media.id
            media = existing_media
            
            # Reset simple fields
            media.status = 'downloading'
            media.title = "Processing..." 
            media.error_message = None
            media.last_played_at = datetime.datetime.now()
            
            # Cleanup old file if exists
            if media.file_path and os.path.exists(media.file_path):
                try:
                    os.remove(media.file_path)
                    print(f"DEBUG: Deleted old file {media.file_path}")
                except Exception as e:
                    print(f"DEBUG: Failed to delete old file: {e}")
            
            db.add(media)
            db.commit()
            db.refresh(media)
        else:
            # Create a placeholder entry in DB
            media = MediaSource(
                title="Processing...",
                source_url=request.url,
                file_path="",
                status="pending",
                owner_id=owner_id
            )
            db.add(media)
            db.commit()
            db.refresh(media)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


from database import engine

def background_download_and_process(url: str, media_id_str: str):
    """
    Handles metadata fetch, download, and AI processing pipeline.
    Updates the existing MediaSource entry.
    """
    media_id = UUID(media_id_str)
    
    # Create a fresh session for this background task
    with Session(engine) as db:
        try:
            # Re-fetch media from DB to ensure it's attached to this session
            media = db.get(MediaSource, media_id)
            if not media:
                print(f"ERROR: Media {media_id} not found in background task.")
                return

            # 1. Fetch Metadata (Async update)
            print(f"DEBUG: Background fetching metadata for {url}...")
            try:
                meta = media_service.fetch_metadata(url)
                media.title = meta.get('title', 'Unknown Title')
                media.duration = meta.get('duration') or 0.0
                media.cover_image = meta.get('thumbnail')
                db.add(media)
                db.commit()
                print(f"DEBUG: Updated metadata for {media.title}")
            except Exception as e:
                print(f"WARN: Background metadata fetch failed: {e}")
                # We continue, as download might still work

            # 1. Download Video
            print(f"DEBUG: Starting download for {media.id}...")
            try:
                local_path = media_service.download_video(url)
            except Exception as e:
                media.status = 'error'
                media.error_message = f"Download Failed: {str(e)}"
                db.add(media)
                db.commit()
                return

            # Update path
            media.file_path = local_path
            media.status = 'processing_audio'
            db.add(media)
            db.commit()
            
            print(f"DEBUG: Processing audio for media {media.id}...")
            
            # 2. Extract Audio
            try:
                audio_path = audio_service.extract_audio(local_path)
                print(f"DEBUG: Audio extracted: {audio_path}")
                
                # 3. Transcribe with Whisper
                media.status = 'transcribing'
                db.add(media)
                db.commit()
                
                print(f"DEBUG: Transcribing audio...")
                segments_data = ai_service.transcribe_audio(audio_path)
                print(f"DEBUG: Transcription complete. {len(segments_data)} segments.")
                
                # 4. Save Segments
                for seg in segments_data:
                    db_seg = SubtitleSegment(
                        media_id=media.id,
                        index=seg['index'],
                        start_time=seg['start_time'],
                        end_time=seg['end_time'],
                        text=seg['text']
                    )
                    db.add(db_seg)
                
                media.status = 'ready' 
                db.add(media)
                db.commit()
                
            except Exception as e:
                print(f"Error in processing pipeline: {e}")
                # We need to re-fetch media if session integrity was lost, but here we are in same transaction block roughly
                media.status = 'error'
                media.error_message = f"Processing failed: {str(e)}"
                db.add(media)
                db.commit()
                
        except Exception as e:
            print(f"Error in background task wrapper: {e}")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Media Source Endpoints ---

@app.get("/media", response_model=List[MediaSource])
def list_media(db: Session = Depends(get_session), owner_id: str = Depends(get_current_owner)):
    statement = select(MediaSource).where(MediaSource.owner_id == owner_id).order_by(MediaSource.created_at.desc())
    results = db.exec(statement).all()
    return results

@app.get("/media/{media_id}", response_model=MediaSource)
def get_media(media_id: UUID, session: Session = Depends(get_session)):
    media = session.get(MediaSource, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@app.post("/media", response_model=MediaSource)
def create_media(media: MediaSource, session: Session = Depends(get_session)):
    session.add(media)
    session.commit()
    session.refresh(media)
    return media

@app.delete("/media/{media_id}")
def delete_media(media_id: UUID, session: Session = Depends(get_session)):
    media = session.get(MediaSource, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Delete local file if exists
    if media.file_path and os.path.exists(media.file_path):
        try:
            os.remove(media.file_path)
            print(f"DEBUG: Deleted file {media.file_path}")
        except Exception as e:
            print(f"WARN: Failed to delete file {media.file_path}: {e}")
            
    # Delete subtitles (if not configured for CASCADE, we delete manually)
    session.exec(select(SubtitleSegment).where(SubtitleSegment.media_id == media_id))
    # Actually, standard SQLModel foreign key needs cascade setup or manual delete.
    # Manual check for safe measure:
    subtitles = session.exec(select(SubtitleSegment).where(SubtitleSegment.media_id == media_id)).all()
    for sub in subtitles:
        session.delete(sub)

    session.delete(media)
    session.commit()
    return {"message": "Media deleted successfully"}

# --- Subtitle Segment Endpoints ---

@app.get("/media/{media_id}/segments", response_model=List[SubtitleSegment])
def list_segments(media_id: UUID, session: Session = Depends(get_session)):
    # Check if media exists
    media = session.get(MediaSource, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    segments = session.exec(
        select(SubtitleSegment)
        .where(SubtitleSegment.media_id == media_id)
        .order_by(SubtitleSegment.index)
    ).all()
    return segments

@app.post("/media/{media_id}/segments", response_model=List[SubtitleSegment])
def create_segments(media_id: UUID, segments: List[SubtitleSegment], session: Session = Depends(get_session)):
    # Check if media exists
    media = session.get(MediaSource, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    for segment in segments:
        segment.media_id = media_id
        session.add(segment)
    
    session.commit()
    return segments

# --- AI Endpoints ---

class LookupRequest(BaseModel):
    word: str
    context: str
    target_language: str = "Chinese" # Default, or detect system locale in frontend

class ExplainRequest(BaseModel):
    text: str
    target_language: str = "Chinese"

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    context: Optional[str] = None
    target_language: str = "Chinese"

@app.post("/ai/lookup-word")
def lookup_word(req: LookupRequest):
    return ai_service.lookup_word(req.word, req.context, req.target_language)

@app.post("/ai/explain")
def explain_context(req: ExplainRequest):
    return ai_service.explain_context(req.text, req.target_language)

@app.post("/ai/chat")
def chat_tutor(req: ChatRequest):
    return ai_service.chat_with_tutor(req.messages, req.context, req.target_language)

# --- Saved Vocab / Notebook Endpoints ---

@app.get("/vocab", response_model=List[SavedWord])
def list_saved_words(
    session: Session = Depends(get_session),
    due_only: bool = False,
    language: Optional[str] = None,
    owner_id: str = Depends(get_current_owner)
):
    query = select(SavedWord).where(SavedWord.owner_id == owner_id)
    
    if language and language != "All": # "All" is a special case from frontend
        query = query.where(SavedWord.language == language)
        
    if due_only:
        query = query.where(SavedWord.next_review_at <= datetime.datetime.utcnow())
        
    query = query.order_by(SavedWord.next_review_at.asc()) # Show due words first
    return session.exec(query).all()

@app.post("/vocab", response_model=SavedWord)
def save_word(word: SavedWord, session: Session = Depends(get_session), owner_id: str = Depends(get_current_owner)):
    try:
        # SQLModel might create the object with string media_id via FastAPI, bypassing strict validation
        if word.media_id and isinstance(word.media_id, str):
            print(f"DEBUG: Manually converting media_id string to UUID: {word.media_id}")
            word.media_id = UUID(word.media_id)
        
        # Enforce owner_id
        word.owner_id = owner_id
        
        session.add(word)
        session.commit()
        session.refresh(word)
        return word
    except Exception as e:
        session.rollback()
        print(f"Error saving word: {e}") 
        # Check for IntegrityError explicitly if possible, or just bad request
        if "foreign key constraint" in str(e).lower():
             raise HTTPException(status_code=400, detail="Invalid Video Reference (ID not found)")
        raise HTTPException(status_code=500, detail=str(e))

class ReviewRequest(BaseModel):
    quality: int # 0-5

@app.post("/vocab/{word_id}/review", response_model=SavedWord)
def review_word(word_id: UUID, req: ReviewRequest, session: Session = Depends(get_session)):
    word = session.get(SavedWord, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
        
    # SM-2 Algorithm Implementation
    q = req.quality
    
    if q < 3: # Review failed, reset
        word.repetitions = 0
        word.interval = 0 # Reset interval
        # Schedule next review in 1 minute (as promised by UI "Again (1m)")
        word.next_review_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    else:
        if word.repetitions == 0:
            word.interval = 1.0
        elif word.repetitions == 1:
            word.interval = 6.0
        else:
            word.interval = word.interval * word.easiness_factor
            
        word.repetitions += 1
        # Update Easiness Factor (EF)
        # EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
        word.easiness_factor = word.easiness_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if word.easiness_factor < 1.3:
            word.easiness_factor = 1.3
            
        # Calculate next review date based on adjusted interval
        word.next_review_at = datetime.datetime.utcnow() + datetime.timedelta(days=word.interval)
    
    session.add(word)
    session.commit()
    session.refresh(word)
    return word

@app.delete("/vocab/{word_id}")
def delete_saved_word(word_id: UUID, session: Session = Depends(get_session)):
    word = session.get(SavedWord, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    session.delete(word)
    session.commit()
    return {"message": "Word deleted"}

if __name__ == "__main__":
    # We use this when running via 'python main.py'
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
