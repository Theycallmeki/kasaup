from fastapi import FastAPI
from app.db import Base, engine

from app.routers import (
    auth,
    users,
    providers,
    services,
    categories,
    appointments
)

app = FastAPI(
    title="Kasaup API",
    version="1.0.0"
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


@app.get("/")
def root():
    return {"message": "Kasaup API running"}