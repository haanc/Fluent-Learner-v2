
from sqlmodel import Session
from database import engine
from models import SavedWord
from uuid import uuid4
import traceback

def debug():
    print("Starting debug save...")
    with Session(engine) as session:
        word = SavedWord(
            id=uuid4(),
            word="DebugWord",
            language="en",
            media_id=None # Explicitly None
        )
        print(f"Created object: {word}")
        try:
            session.add(word)
            session.commit()
            session.refresh(word)
            print("Success!")
        except Exception as e:
            print("Caught Exception!")
            traceback.print_exc()

if __name__ == "__main__":
    debug()
