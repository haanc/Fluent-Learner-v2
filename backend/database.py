import os
from sqlmodel import create_engine, SQLModel, Session
import models # Removed relative import

# Use a local sqlite file in the backend directory, resolving relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(base_dir, "learning.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
