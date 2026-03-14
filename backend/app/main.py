from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.core.config import settings

from app.routers import (
    auth,
    users,
    providers,
    services,
    categories,
    appointments,
    provider_availability
)

app = FastAPI(
    title="Kasaup API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
def root():
    return {"message": "Kasaup API running"}