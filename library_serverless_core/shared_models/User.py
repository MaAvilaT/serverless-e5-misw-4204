from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..persistence.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    username = Column(String)
    password = Column("pass", String)
    role_id = Column(ForeignKey("roles.id"))
    email = Column(String)

    role = relationship('Role', back_populates="users")

    videos = relationship('Video', back_populates='user', cascade='all, delete, delete-orphan')
