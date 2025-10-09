from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schema.user_schema import UserCreate, UserResponse
from src.controller.user_controller import create_user 




class UserApi:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=UserResponse)
        def create_user_endpoint(user:UserCreate, db: Session = Depends(get_db)):
            return create_user(user, db)
