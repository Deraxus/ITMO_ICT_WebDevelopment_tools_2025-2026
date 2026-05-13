from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.destinations import router as destinations_router
from app.api.routes.skills import router as skills_router
from app.api.routes.trip_participants import router as trip_participants_router
from app.api.routes.trips import router as trips_router
from app.api.routes.users import router as users_router


app = FastAPI(
    title="Travel Buddy API",
    description="API for searching travel partners",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(destinations_router)
app.include_router(trip_participants_router)
app.include_router(trips_router)


@app.get("/")
def root():
    return {"message": "Travel Buddy API is running"}