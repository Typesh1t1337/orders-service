from api.v1.handlers.orders import (create_order, get_order_by_id,
                                    get_orders_by_user_id, update_order_by_id)
from .router import Router
from fastapi import APIRouter


class UsersRouter(Router):
    def __init__(self):
        super().__init__(router=APIRouter(prefix="/api", tags=["Users"]))

    def add_router(self):
        self.router.add_api_route(path="/order", status_code=201,
                                  endpoint=create_order, methods=["POST"])
        self.router.add_api_route(path="/order/{id}", status_code=200,
                                  endpoint=get_order_by_id, methods=["GET"])
        self.router.add_api_route(path="/user/order", status_code=200,
                                  endpoint=get_orders_by_user_id, methods=["GET"])
        self.router.add_api_route(path="/order/{id}", status_code=200,
                                  endpoint=update_order_by_id, methods=["PATCH"])


router = UsersRouter().router
