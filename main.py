from fastapi import FastAPI


class AppFactory:
    def __init__(self):
        self.app = FastAPI()

    def get_app(self):
        return self.app


app_factory = AppFactory()
app = app_factory.get_app()

