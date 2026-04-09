from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud import (
    create_destination,
    delete_destination,
    get_destination_by_id,
    get_destinations,
    get_trip_by_id,
    update_destination
)
from app.db import get_db
from app.models.user import User
from app.schemas.destination import DestinationCreate, DestinationRead, DestinationUpdate


router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.post("/trip/{trip_id}", response_model=DestinationRead, status_code=status.HTTP_201_CREATED)
def create_destination_endpoint(
    trip_id: int,
    destination_data: DestinationCreate,
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
            detail="Only the trip owner can add destinations"
        )

    return create_destination(db, trip_id, destination_data)


@router.get("/", response_model=list[DestinationRead])
def get_destinations_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_destinations(db)


@router.get("/{destination_id}", response_model=DestinationRead)
def get_destination_endpoint(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    return destination


@router.put("/{destination_id}", response_model=DestinationRead)
def update_destination_endpoint(
    destination_id: int,
    destination_data: DestinationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )

    trip = get_trip_by_id(db, destination.trip_id)
    if trip.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip owner can update destinations"
        )

    return update_destination(db, destination, destination_data)


@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_destination_endpoint(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )

    trip = get_trip_by_id(db, destination.trip_id)
    if trip.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the trip owner can delete destinations"
        )

    delete_destination(db, destination)