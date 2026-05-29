from sqlalchemy.orm import Session, selectinload

from app.models.user import User
from app.models.user_skill import UserSkill
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .options(
            selectinload(User.trips_created),
            selectinload(User.skills).selectinload(UserSkill.skill)
        )
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(db: Session, user_data: UserCreate, hashed_password: str) -> User:
    user = User(
        email=user_data.email,
        name=user_data.name,
        bio=user_data.bio,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()

def update_user_password(db: Session, user: User, hashed_password: str) -> User:
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user