from sqlalchemy.orm import Session, selectinload

from app.models.trip_participant import TripParticipant
from app.schemas.trip_participant import TripParticipantCreate, TripParticipantUpdate


def get_trip_participant_by_id(db: Session, participant_id: int) -> TripParticipant | None:
    return (
        db.query(TripParticipant)
        .options(selectinload(TripParticipant.user))
        .filter(TripParticipant.id == participant_id)
        .first()
    )


def get_trip_participants(db: Session) -> list[TripParticipant]:
    return (
        db.query(TripParticipant)
        .options(selectinload(TripParticipant.user))
        .all()
    )


def get_trip_participants_by_trip_id(db: Session, trip_id: int) -> list[TripParticipant]:
    return (
        db.query(TripParticipant)
        .options(selectinload(TripParticipant.user))
        .filter(TripParticipant.trip_id == trip_id)
        .all()
    )


def create_trip_participant(
    db: Session,
    trip_id: int,
    participant_data: TripParticipantCreate
) -> TripParticipant:
    participant = TripParticipant(
        user_id=participant_data.user_id,
        trip_id=trip_id,
        status=participant_data.status,
        message=participant_data.message
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def update_trip_participant(
    db: Session,
    participant: TripParticipant,
    participant_data: TripParticipantUpdate
) -> TripParticipant:
    update_data = participant_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(participant, field, value)

    db.commit()
    db.refresh(participant)
    return participant


def delete_trip_participant(db: Session, participant: TripParticipant) -> None:
    db.delete(participant)
    db.commit()