from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.event_api import EventAPI
from src.config.database import Base, engine, session_local
from src.model.event import Event, Sport, Location
from devfakedata.seed import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    # DÉMARRAGE
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        seed(db)  # <- seed une seule fois
    finally:
        db.close()

    yield



app = FastAPI(lifespan=lifespan)

# Création des tables
# Base.metadata.create_all(bind=engine)

# API init
event_api = EventAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    event_api.router,
    prefix="/event",
    tags=["Event"]
)


