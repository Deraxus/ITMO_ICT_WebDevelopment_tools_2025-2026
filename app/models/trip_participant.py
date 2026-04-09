from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class TripParticipant(Base):
    __tablename__ = "trip_participants"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))

    status = Column(String, default="pending")
    message = Column(String, nullable=True)

    user = relationship("User", back_populates="trips_participating")
    trip = relationship("Trip", back_populates="participants")