from datetime import datetime
from typing import List, Optional

from pydantic import UUID4
from starlite import Controller, Partial, delete, get, patch, post, put

from app.models import CreateUser, User


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: CreateUser) -> CreateUser:
        # TODO:
        # - Create/register user to database
        # - Secure user account by hiding information (i.e. mask email and password)
        return data

    @get()
    async def list_users(self) -> List[User]:
        ...

    @get(path="/{date:int}")
    async def list_new_users(self, date: datetime) -> List[User]:
        ...

    @patch(path="/{user_id:uuid}")
    async def partially_update_user(self, user_id: UUID4, data: Partial[User]) -> User:
        ...

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User:
        ...

    @get(path="/{user_name:str}")
    async def get_user_by_name(self, user_name: str) -> Optional[User]:
        ...

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User:
        ...

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> User:
        ...
