from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)

    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    trip_id = Column(Integer, ForeignKey("trips.id"))

    trip = relationship("Trip", back_populates="destinations")