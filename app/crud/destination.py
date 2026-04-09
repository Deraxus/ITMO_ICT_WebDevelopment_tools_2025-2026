from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.schemas.destination import DestinationCreate, DestinationUpdate


def get_destination_by_id(db: Session, destination_id: int) -> Destination | None:
    return db.query(Destination).filter(Destination.id == destination_id).first()


def get_destinations(db: Session) -> list[Destination]:
    return db.query(Destination).all()


def get_destinations_by_trip_id(db: Session, trip_id: int) -> list[Destination]:
    return db.query(Destination).filter(Destination.trip_id == trip_id).all()


def create_destination(
    db: Session,
    trip_id: int,
    destination_data: DestinationCreate
) -> Destination:
    destination = Destination(
        city=destination_data.city,
        country=destination_data.country,
        trip_id=trip_id
    )
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


def update_destination(
    db: Session,
    destination: Destination,
    destination_data: DestinationUpdate
) -> Destination:
    update_data = destination_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(destination, field, value)

    db.commit()
    db.refresh(destination)
    return destination


def delete_destination(db: Session, destination: Destination) -> None:
    db.delete(destination)
    db.commit()