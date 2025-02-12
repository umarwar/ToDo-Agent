from sqlalchemy import create_engine, Column, Integer, String, select, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    todo = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
