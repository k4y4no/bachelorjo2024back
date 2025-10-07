from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from src.config.database import Base, get_db
from src.model.event import Sport, Location
import pytest


# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    sport = Sport(name="Athlétisme")
    location = Location(name="Stade de France", nb_places=80000)
    database.add(sport)
    database.add(location)
    database.commit()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


#Fisture to setup and teardown the database for each test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)