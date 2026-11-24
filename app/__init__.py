import os

from flask import Flask

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "clave-local-solo-desarrollo"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

from app import rutas