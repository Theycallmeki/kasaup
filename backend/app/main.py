from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import Base, engine
from app.core.config import settings

from app.routers import (
    auth,
    users,
    providers,
    services,
    categories,
    appointments,
    provider_availability,
    ratings,
    messages
)

app = FastAPI(
    title="Kasaup API",
    version="1.0.0"
)

origins = settings.cors_origins()

print("CORS ORIGINS:", origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(providers.router, prefix="/providers", tags=["Providers"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(provider_availability.router, prefix="/availability", tags=["Provider Availability"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])


@app.get("/")
def root():
    return {"message": "Kasaup API running"}