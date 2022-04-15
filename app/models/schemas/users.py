from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel  # type: ignore


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    password: str
    username: str
