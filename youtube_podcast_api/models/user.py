from sqlalchemy import Column, Integer, String, Boolean

from youtube_podcast_api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_google_id = Column(String, unique=True, index=True)
    token = Column(String)
    admin = Column(Boolean, default=False)
