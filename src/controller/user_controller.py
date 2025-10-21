import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.schema.user_schema import UserCreate, UserLogin, UserResponse
from src.service.auth_service import get_user_by_email
from src.config.hash import pwd_context
from src.model.user import User, Role



def create_user(user: UserCreate, db: Session):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already used"
        )
    hashed_password = pwd_context.hash(user.password)
    secret_key = secrets.token_urlsafe(32)  # Génère une clé secrète aléatoire
    # Récupère le rôle "user" (ou adapte selon ton besoin)
    role = db.query(Role).filter_by(name="user").first()
    new_user = User(
        name=user.name,
        firstname=user.firstname,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        hidden_key=secret_key,
        roles=[role]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        firstname=new_user.firstname,
        email=new_user.email,
        phone=new_user.phone,
        roles=[r.name for r in new_user.roles]
    ).model_dump()