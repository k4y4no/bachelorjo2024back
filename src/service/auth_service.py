from sqlalchemy.orm import Session


from src.model.user import User


def get_user_by_email(email:str, db: Session):
    return db.query(User).filter(User.email == email).first()