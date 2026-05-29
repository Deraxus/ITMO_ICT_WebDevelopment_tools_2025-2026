from pydantic import BaseModel, ConfigDict

from app.schemas.destination import DestinationCreate, DestinationRead
from app.schemas.trip_participant import TripParticipantWithUser
from app.schemas.user import UserShort


class TripBase(BaseModel):
    title: str
    description: str | None = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class TripRead(TripBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TripWithDestinations(TripRead):
    destinations: list[DestinationRead] = []

    model_config = ConfigDict(from_attributes=True)


class TripWithParticipants(TripRead):
    participants: list[TripParticipantWithUser] = []

    model_config = ConfigDict(from_attributes=True)


class TripDetailed(TripRead):
    owner: UserShort
    destinations: list[DestinationRead] = []
    participants: list[TripParticipantWithUser] = []

    model_config = ConfigDict(from_attributes=True)