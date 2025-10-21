from passlib.context import CryptContext


ACCESS_TOKEN_EXPIRE_MINUTES = 10
ALGORITHM = "HS256"
SECRET_KEY = "5prJmFDk0LhRLFScFfSaI9IOVWd"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")