import os
from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount
from fastapi_app.main import app as fastapi_app
from starlette.staticfiles import StaticFiles

# Ensure the DJANGO_SETTINGS_MODULE environment variable is set correctly.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TiluBee.settings")

# Get the standard Django ASGI application.
django_app = get_asgi_application()

# Wrap django_app in a lambda to match the expected ASGI callable signature
django_app_wrapper = lambda scope, receive, send: django_app(scope, receive, send)


# Define the routing: mount FastAPI on '/fastapi' and Django on '/'.
routes = [
    Mount("/api", app=fastapi_app),
    Mount("/", app=django_app_wrapper),
    Mount("/static", app=StaticFiles(directory="static"), name="static")
]

# Create a Starlette application that dispatches to the mounted apps.
application = Starlette(routes=routes)
