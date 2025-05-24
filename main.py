from fastapi import FastAPI
from db.base import engine, Base
from middlewares.auth import AuthMiddleware
from api.v1.routers.user_orders import router as user_orders_router


class AppFactory:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_event_handler(event_type="startup", func=self.on_startup)
        self.register_middleware()
        self.register_routers()

    def register_routers(self):
        self.app.include_router(router=user_orders_router)

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)