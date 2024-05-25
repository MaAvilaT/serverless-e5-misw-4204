import datetime
import sqlalchemy
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..persistence.database import Base
from . import User


class VideoStatus(enum.Enum):
    processed: str = "processed"
    uploaded: str = "uploaded"


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(String)
    status = Column(sqlalchemy.Enum(VideoStatus))
    timestamp = Column(DateTime, default=datetime.datetime.now())

    user = relationship('User', back_populates='videos')
