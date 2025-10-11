from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schema.user_schema import  UserLogin
from src.controller.auth_controller import check_token, login_user, logout_user
from src.schema.token_schema import Token





class AuthApi:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):
    
        @self.router.post(path="/", response_model=Token)
        def login(user: UserLogin,  db: Session = Depends(get_db)):
            return login_user(user, db)
        
                
        @self.router.post(path="/logout")
        def logout():
            return logout_user()
        
        @self.router.get(path="/check",  response_model=dict)
        def check(request: Request):
            return check_token(request)
