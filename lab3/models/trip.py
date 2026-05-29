from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # связи
    owner = relationship("User", back_populates="trips_created")

    destinations = relationship(
        "Destination",
        back_populates="trip",
        cascade="all, delete"
    )

    participants = relationship(
        "TripParticipant",
        back_populates="trip"
    )