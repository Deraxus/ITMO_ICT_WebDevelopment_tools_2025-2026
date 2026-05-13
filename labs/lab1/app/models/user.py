from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    # связи
    trips_created = relationship("Trip", back_populates="owner")

    trips_participating = relationship(
        "TripParticipant",
        back_populates="user"
    )

    skills = relationship(
        "UserSkill",
        back_populates="user"
    )