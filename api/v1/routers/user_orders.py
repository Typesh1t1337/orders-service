from api.v1.handlers.orders import create_order
from .router import Router
from fastapi import APIRouter


class UsersRouter(Router):
    def __init__(self):
        super().__init__(router=APIRouter(prefix="/api", tags=["Users"]))

    def add_router(self):
        self.router.add_api_route(path="/order", status_code=201,
                                  endpoint=create_order, methods=["POST"])


router = UsersRouter().router
