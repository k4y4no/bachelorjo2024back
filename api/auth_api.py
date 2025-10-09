from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schema.user_schema import  UserLogin
from src.controller.auth_controller import login_user
from src.schema.token_schema import Token





class AuthApi:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
    
        @self.router.post(path="/", response_model=Token)
        def login(user: UserLogin,  db: Session = Depends(get_db)):
            return login_user(user, db)