# База данных

Используется PostgreSQL и ORM SQLAlchemy.

## Основные сущности:

### User
- id
- email
- name
- bio
- hashed_password

### Trip
- id
- title
- description
- owner_id

### Destination
- id
- city
- country
- trip_id

### Skill
- id
- name

### TripParticipant
- id
- user_id
- trip_id
- status
- message

# База данных

Используется PostgreSQL + SQLAlchemy ORM.

## Модель User

    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, nullable=False)
        name = Column(String)
        bio = Column(String)
        hashed_password = Column(String, nullable=False)

## Модель Trip

    class Trip(Base):
        __tablename__ = "trips"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String, nullable=False)
        description = Column(String)
        owner_id = Column(Integer, ForeignKey("users.id"))

## Ассоциативная таблица

    class TripParticipant(Base):
        __tablename__ = "trip_participants"

        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        trip_id = Column(Integer, ForeignKey("trips.id"))
        status = Column(String)
        message = Column(String)

## Связи

- User → Trip (one-to-many)
- Trip → Destination (one-to-many)
- User ↔ Trip (many-to-many через TripParticipant)
