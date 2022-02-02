from flask import Blueprint
from app.controllers import anime_controler

bp_animes = Blueprint("animes", __name__, url_prefix="/animes")

bp_animes.post("")(anime_controler.create)

bp_animes.get("")(anime_controler.get_animes)

bp_animes.get("/<int:id>")(anime_controler.get_animes_by_id)

bp_animes.patch("/<int:id>")(anime_controler.update_anime)

bp_animes.delete("/<int:id>")(anime_controler.delete)