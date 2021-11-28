from falcon.asgi import App
from falcon import CORSMiddleware
from .handlers import Basic


def create_app():
    app = App(middleware=CORSMiddleware())
    app.add_route('/', Basic())
    return app
