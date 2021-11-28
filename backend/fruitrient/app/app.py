from falcon.asgi import App
from .handlers import Basic


def create_app():
    app = App()
    app.add_route('/', Basic())
    return app
