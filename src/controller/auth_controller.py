from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.schema.user_schema import UserLogin
from src.service.auth_service import get_user_by_email
from src.service.token_service import create_token
from src.config.hash import pwd_context



def login_user(user: UserLogin, db: Session):
    db_user = get_user_by_email(
        db=db,
        email=user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    if pwd_context.verify(user.password, db_user.password): 
        return create_token(data={
            "id_sub": db_user.id,
            "sub": user.email,
            # "role": db_user.role
            })
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"

        )
