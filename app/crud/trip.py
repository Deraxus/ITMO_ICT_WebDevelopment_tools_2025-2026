from sqlalchemy.orm import Session, selectinload

from app.models.destination import Destination
from app.models.trip import Trip
from app.models.trip_participant import TripParticipant
from app.schemas.trip import TripCreate, TripUpdate


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    return (
        db.query(Trip)
        .options(
            selectinload(Trip.owner),
            selectinload(Trip.destinations),
            selectinload(Trip.participants).selectinload(TripParticipant.user)
        )
        .filter(Trip.id == trip_id)
        .first()
    )


def get_trips(db: Session) -> list[Trip]:
    return (
        db.query(Trip)
        .options(
            selectinload(Trip.owner),
            selectinload(Trip.destinations),
            selectinload(Trip.participants).selectinload(TripParticipant.user)
        )
        .all()
    )


def get_trips_by_owner_id(db: Session, owner_id: int) -> list[Trip]:
    return (
        db.query(Trip)
        .options(
            selectinload(Trip.owner),
            selectinload(Trip.destinations),
            selectinload(Trip.participants).selectinload(TripParticipant.user)
        )
        .filter(Trip.owner_id == owner_id)
        .all()
    )


def search_trips(
    db: Session,
    destination_city: str | None = None,
    country: str | None = None
) -> list[Trip]:
    query = (
        db.query(Trip)
        .options(
            selectinload(Trip.owner),
            selectinload(Trip.destinations),
            selectinload(Trip.participants).selectinload(TripParticipant.user)
        )
    )

    if destination_city or country:
        query = query.join(Destination)

        if destination_city:
            query = query.filter(Destination.city.ilike(f"%{destination_city}%"))

        if country:
            query = query.filter(Destination.country.ilike(f"%{country}%"))

    return query.distinct().all()


def create_trip(db: Session, trip_data: TripCreate, owner_id: int) -> Trip:
    trip = Trip(
        title=trip_data.title,
        description=trip_data.description,
        owner_id=owner_id
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def update_trip(db: Session, trip: Trip, trip_data: TripUpdate) -> Trip:
    update_data = trip_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(trip, field, value)

    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip: Trip) -> None:
    db.delete(trip)
    db.commit()