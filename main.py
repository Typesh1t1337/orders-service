from fastapi import FastAPI
from db.base import engine, Base
from middlewares.auth import AuthMiddleware


class AppFactory:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_event_handler(event_type="startup", func=self.on_startup)
        self.register_middleware()
        self.register_routers()

    def register_routers(self):
        pass

    def register_middleware(self):
        self.app.add_middleware(
            middleware_class=AuthMiddleware
        )

    def get_app(self):
        return self.app

    @staticmethod
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


app_factory = AppFactory()
app = app_factory.get_app()

