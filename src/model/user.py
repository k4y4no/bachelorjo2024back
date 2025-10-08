from src.config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id: Mapped[int]  = mapped_column(ForeignKey('users.id'), primary_key=True)
    role_id: Mapped[int]  = mapped_column(ForeignKey('roles.id'), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int]  = mapped_column( primary_key=True)
    name: Mapped[str] = mapped_column(String)
    firstname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    hidden_key: Mapped[str] = mapped_column(String)
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int]  = mapped_column( primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

