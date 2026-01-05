
from sqlmodel import SQLModel, Session, create_engine
from models import SavedWord
import uuid
import datetime

# Setup in-memory DB for reproduction
sqlite_url = "sqlite:///./test.db"
engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)

def repro():
    # Simulate payload as Dictionary (what FastAPI receives)
    payload = {
        "word": "expectations",
        "context_sentence": "So, okay, that actually beat my expectations,",
        # "media_id": "5ead9b76-23d0-453b-a931-607076953732", # Passed as string
        "media_id": str(uuid.uuid4()),
        "media_time": 54.9,
        "language": "en"
    }

    print("Creating SavedWord from payload...")
    try:
        # Pydantic validation happens here
        word_obj = SavedWord(**payload) 
        print(f"Object created. media_id type: {type(word_obj.media_id)}")
        print(f"media_id value: {word_obj.media_id}")
    except Exception as e:
        print(f"Pydantic Error: {e}")
        return

    print("Attempting to save to DB...")
    with Session(engine) as session:
        try:
            session.add(word_obj)
            session.commit()
            session.refresh(word_obj)
            print("Successfully saved!")
        except Exception as e:
            print(f"DB Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    repro()
