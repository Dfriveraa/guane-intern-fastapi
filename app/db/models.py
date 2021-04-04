from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hashed = Column(String)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    adopted_dogs = relationship("Dog", back_populates="adopter", foreign_keys="Dog.adopter_id")
    registered_dogs = relationship("Dog", back_populates="publisher", foreign_keys="Dog.publisher_id")


class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    picture = Column(String)
    is_adopted = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now())
    publisher_id = Column(Integer, ForeignKey("users.id"))
    adopter_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship("User", back_populates="registered_dogs", foreign_keys=[publisher_id])
    adopter = relationship("User", back_populates="adopted_dogs", foreign_keys=[adopter_id])


Base.metadata.create_all(bind=engine)
