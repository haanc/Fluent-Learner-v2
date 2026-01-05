
from database import engine
from models import MediaSource
from sqlmodel import Session, select

def list_media():
    with Session(engine) as session:
        statement = select(MediaSource)
        results = session.exec(statement).all()
        print(f"Total Media in DB: {len(results)}")
        for media in results:
            print(f"ID: {media.id} | Title: {media.title} | Status: {media.status}")

if __name__ == "__main__":
    list_media()
