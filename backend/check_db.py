from sqlmodel import Session, select
from database import engine
from models import MediaSource
import json

def check_db():
    with Session(engine) as session:
        statement = select(MediaSource)
        results = session.exec(statement).all()
        
        media_info = []
        for media in results:
            info = {
                "id": str(media.id),
                "title": media.title,
                "status": media.status,
                "file_path": media.file_path,
                "error_message": media.error_message,
                "source_url": media.source_url,
                "subtitles_count": len(media.segments)
            }
            media_info.append(info)
            
        print(json.dumps(media_info, indent=2))

if __name__ == "__main__":
    check_db()
