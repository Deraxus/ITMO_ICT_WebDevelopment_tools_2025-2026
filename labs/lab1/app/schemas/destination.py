from pydantic import BaseModel, ConfigDict


class DestinationBase(BaseModel):
    city: str
    country: str


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    city: str | None = None
    country: str | None = None


class DestinationRead(DestinationBase):
    id: int
    trip_id: int

    model_config = ConfigDict(from_attributes=True)