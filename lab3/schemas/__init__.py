from .user import UserCreate, UserRead, UserUpdate, UserShort
from .skill import SkillCreate, SkillRead
from .destination import DestinationCreate, DestinationRead, DestinationUpdate
from .trip_participant import (
    TripParticipantCreate,
    TripParticipantRead,
    TripParticipantUpdate,
    TripParticipantWithUser
)
from .trip import (
    TripCreate,
    TripRead,
    TripUpdate,
    TripWithDestinations,
    TripWithParticipants,
    TripDetailed
)
from .auth import Token, LoginRequest, ChangePasswordRequest