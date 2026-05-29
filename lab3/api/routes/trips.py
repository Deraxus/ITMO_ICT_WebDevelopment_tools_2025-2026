from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud import (
    create_trip,
    delete_trip,
    get_trip_by_id,
    get_trips,
    get_trips_by_owner_id,
    get_user_by_id,
    search_trips,
    update_trip
)
from app.db import get_db
from app.models.user import User
from app.schemas.trip import TripCreate, TripDetailed, TripRead, TripUpdate


router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/", response_model=TripRead, status_code=status.HTTP_201_CREATED)
def create_trip_endpoint(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_trip(db, trip_data, owner_id=current_user.id)


@router.get("/", response_model=list[TripDetailed])
def get_trips_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_trips(db)


@router.get("/search", response_model=list[TripDetailed])
def search_trips_endpoint(
    destination_city: str | None = Query(default=None),
    country: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_trips(db, destination_city=destination_city, country=country)


@router.get("/owner/{owner_id}", response_model=list[TripDetailed])
def get_trips_by_owner_endpoint(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    owner = get_user_by_id(db, owner_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner user not found"
        )

    return get_trips_by_owner_id(db, owner_id)


@router.get("/{trip_id}", response_model=TripDetailed)
def get_trip_endpoint(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    return trip


@router.put("/{trip_id}", response_model=TripRead)
def update_trip_endpoint(
    trip_id: int,
    trip_data: TripUpdate,
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
            detail="Only the trip owner can update this trip"
        )

    return update_trip(db, trip, trip_data)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip_endpoint(
    trip_id: int,
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
            detail="Only the trip owner can delete this trip"
        )

    delete_trip(db, trip)