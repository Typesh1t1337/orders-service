from fastapi import APIRouter


class Router:
    def __init__(self, router: APIRouter):
        self.router: APIRouter = router
        self.add_router()

    def add_router(self):
        raise NotImplementedError()

