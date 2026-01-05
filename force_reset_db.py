
import sys
import os
from sqlmodel import create_engine, SQLModel, Session, select, inspect

# Use same DB name
sqlite_file_name = "backend/learning.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

# Import models to ensure they are registered with SQLModel
# We need to add backend to sys.path since we run from root
sys.path.append(os.path.join(os.getcwd(), "backend"))
from models import MediaSource

def reset_and_verify():
    print(f"Checking DB at: {os.path.abspath(sqlite_file_name)}")
    
    # 1. Create Tables
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    
    # 2. Inspect Schema
    print("Inspecting schema...")
    insp = inspect(engine)
    columns = [c['name'] for c in insp.get_columns('mediasource')]
    print(f"Columns in MediaSource: {columns}")
    
    if "source_url" in columns:
        print("SUCCESS: source_url column exists!")
    else:
        print("FAILURE: source_url missing!")
        sys.exit(1)

if __name__ == "__main__":
    reset_and_verify()
