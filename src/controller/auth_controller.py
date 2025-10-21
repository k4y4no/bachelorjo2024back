from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from src.service.token_service import verify_token
from fastapi.responses import JSONResponse

from src.schema.user_schema import UserLogin, UserResponse
from src.service.auth_service import get_user_by_email
from src.service.token_service import create_token
from src.config.hash import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context



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
        token = create_token(data={
            "id_sub": db_user.id,
            "sub": user.email,
            # "role": db_user.role
            })
        response = JSONResponse(content={
            "message": "Connexion réussie",
            "user": UserResponse(
                id=db_user.id,
                name=db_user.name,
                firstname=db_user.firstname,
                email=db_user.email,
                phone=db_user.phone,
                roles=[role.name for role in db_user.roles]
            ).model_dump()
            })
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            secure=True,  # à activer en production (HTTPS)
            samesite="none",
            max_age=60 * ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"

        )
    
def logout_user():
    response = JSONResponse(content={"message": "Déconnexion réussie"})
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,  # adapte selon ton environnement
        samesite="none",
        max_age=0
    )
    return response
    
def check_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant"
        )
    try:
        payload = verify_token(token)
        return {"valid": True, "payload": payload}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )
