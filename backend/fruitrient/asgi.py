# Author: Ruthger 

from .app.app import create_app

# Create an app instance to be executed by the ASGI framework (e.g. daphne)
app = create_app()
