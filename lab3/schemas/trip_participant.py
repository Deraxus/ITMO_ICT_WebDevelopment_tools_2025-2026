from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserShort


class TripParticipantBase(BaseModel):
    user_id: int
    trip_id: int
    status: str = "pending"
    message: str | None = None


class TripParticipantCreate(BaseModel):
    user_id: int
    status: str = "pending"
    message: str | None = None


class TripParticipantUpdate(BaseModel):
    status: str | None = None
    message: str | None = None


class TripParticipantRead(TripParticipantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TripParticipantWithUser(BaseModel):
    id: int
    status: str
    message: str | None = None
    user: UserShort

    model_config = ConfigDict(from_attributes=True)