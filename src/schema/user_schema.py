from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserCreate(UserLogin):
    name: str
    firstname:str
    phone: str



class UserResponse(BaseModel):
    email: str
    name: str
    firstname:str
    phone: str
    id: int

    class ConfigDict:
        from_attributes = True