from fastapi import FastAPI
from db.base import engine, Base


class AppFactory:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_event_handler(event_type="startup", func=self.on_startup)

    def get_app(self):
        return self.app

    async def on_startup(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


app_factory = AppFactory()
app = app_factory.get_app()

