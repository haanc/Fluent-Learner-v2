from sqlmodel import Session, select, create_engine
from database import engine
from models import MediaSource
from uuid import uuid4
import datetime
import os

# Mock URL
request_url = "https://www.youtube.com/watch?v=2V9VjbcjQuw"

def test_import():
    print("Starting import test...")
    with Session(engine) as db:
        try:
            # 1. Select
            print("1. Executing select...")
            statement = select(MediaSource).where(MediaSource.source_url == request_url)
            existing_media = db.exec(statement).first()
            print(f"2. Select result: {existing_media}")

            if existing_media:
                print("   Found existing.")
                # Logic from main.py
                if existing_media.file_path and os.path.exists(existing_media.file_path):
                    try:
                        os.remove(existing_media.file_path)
                    except Exception as e:
                        print(f"   Remove error: {e}")
            else:
                print("   Not found, creating new.")
                media_id = uuid4()
                media = MediaSource(
                    id=media_id,
                    title="Processing...",
                    source_url=request_url,
                    file_path="", 
                    duration=0.0,
                    language='en',
                    cover_image=None,
                    status='downloading', 
                    created_at=datetime.datetime.now(),
                    last_played_at=datetime.datetime.now()
                )
                db.add(media)
                print("3. Committing...")
                db.commit()
                db.refresh(media)
                print(f"4. Success! ID: {media.id}")

        except Exception as e:
            print(f"CRASH: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_import()
