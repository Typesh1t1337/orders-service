from sqlalchemy.testing.pickleable import User

from .router import Router
from fastapi import APIRouter


class UsersRouter(Router):
    def __init__(self):
        super().__init__(router=APIRouter(prefix="/api", tags=["Users"]))

    def add_router(self):
        pass