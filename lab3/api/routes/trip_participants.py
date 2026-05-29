from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud import (
    create_trip_participant,
    delete_trip_participant,
    get_trip_by_id,
    get_trip_participant_by_id,
    get_trip_participants,
    get_user_by_id,
    update_trip_participant
)
from app.db import get_db
from app.models.user import User
from app.schemas.trip_participant import (
    TripParticipantCreate,
    TripParticipantRead,
    TripParticipantUpdate
)


router = APIRouter(prefix="/trip-participants", tags=["Trip Participants"])


@router.post("/trip/{trip_id}", response_model=TripParticipantRead, status_code=status.HTTP_201_CREATED)
def create_trip_participant_endpoint(
    trip_id: int,
    participant_data: TripParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    if trip.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip owner can add participants"
        )

    user = get_user_by_id(db, participant_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    for existing_participant in trip.participants:
        if existing_participant.user_id == participant_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already added to this trip"
            )

    return create_trip_participant(db, trip_id, participant_data)


@router.get("/", response_model=list[TripParticipantRead])
def get_trip_participants_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_trip_participants(db)


@router.get("/{participant_id}", response_model=TripParticipantRead)
def get_trip_participant_endpoint(
    participant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    participant = get_trip_participant_by_id(db, participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip participant not found"
        )
    return participant


@router.put("/{participant_id}", response_model=TripParticipantRead)
def update_trip_participant_endpoint(
    participant_id: int,
    participant_data: TripParticipantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    participant = get_trip_participant_by_id(db, participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip participant not found"
        )

    trip = get_trip_by_id(db, participant.trip_id)
    if trip.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip owner can update participants"
        )

    return update_trip_participant(db, participant, participant_data)


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip_participant_endpoint(
    participant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    participant = get_trip_participant_by_id(db, participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip participant not found"
        )

    trip = get_trip_by_id(db, participant.trip_id)
    if trip.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip owner can delete participants"
        )

    delete_trip_participant(db, participant)