from flask import Flask
from app.routes.anime_blueprint import bp_animes


def init_app(app:Flask):
    app.register_blueprint(bp_animes)