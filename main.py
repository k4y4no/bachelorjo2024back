from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import ProxyHeadersMiddleware

from api import offer_api
from api.event_api import EventAPI
from api.user_api import UserApi
from api.auth_api import AuthApi
from api.offer_api import OfferTicketAPI
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
user_api = UserApi()
auth_api = AuthApi()
offer_api = OfferTicketAPI()

# Trust proxy headers (X-Forwarded-Proto) so redirects keep https scheme
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# CORS access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://jofront-116031105986.europe-west1.run.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    event_api.router,
    prefix="/event",
    tags=["Event"]
)

app.include_router(
    user_api.router,
    prefix="/user",
    tags=["User"]
)

app.include_router(
    auth_api.router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    offer_api.router,
    prefix="/offer",
    tags=["Offer"]
)
