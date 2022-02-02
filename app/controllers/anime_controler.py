from flask import jsonify, request
from app.models.anime_model import Animes
from http import HTTPStatus
from psycopg2.errors import UniqueViolation, UndefinedColumn


def create():
    data = request.get_json()

    try:
        anime = Animes(data["anime"],data["released_date"], data["seasons"])
        inserted_anime = anime.create_anime()
    except KeyError:
        anime_keys = ["anime", "released_date", "seasons"]
        data_keys = list(data.keys())
        wrong_keys = []
        for key in data_keys:
            if not key in anime_keys:
                wrong_keys.append(key)

        return {"avaliable_keys": anime_keys, "wrong_keys_sended": wrong_keys}, HTTPStatus.UNPROCESSABLE_ENTITY
    except UniqueViolation:
        return {"error": "anime já existe"}, HTTPStatus.UNPROCESSABLE_ENTITY
    
        
    anime_key = ["id", "anime", "released_date", "seasons"]
    inserted_anime = dict(zip(anime_key, inserted_anime))

    return jsonify(inserted_anime), HTTPStatus.CREATED

def get_animes():
    animes = Animes.read_anime()

    anime_key = ["id", "anime", "released_date", "seasons"]

    anime_list = [dict(zip(anime_key, anime)) for anime in animes]

    return jsonify(anime_list), HTTPStatus.OK


def get_animes_by_id(id):
    animes = Animes.read_anime_by_id(id)

    anime_key = ["id", "anime", "released_date", "seasons"]

    anime_list = [dict(zip(anime_key, anime)) for anime in animes]

    if anime_list == []:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND
    return jsonify(anime_list), HTTPStatus.OK

def update_anime(id):
    payload = request.get_json()
    try:
        if "anime" in list(payload.keys()):
            payload["anime"] = payload["anime"].title()
        updated_anime = Animes.update_anime(id, payload)
    except UndefinedColumn:
        anime_keys = ["anime", "released_date", "seasons"]
        data_keys = list(payload.keys())
        wrong_keys = []
        for key in data_keys:
            if not key in anime_keys:
                wrong_keys.append(key)

        return {"avaliable_keys": anime_keys, "wrong_keys_sended": wrong_keys}, HTTPStatus.UNPROCESSABLE_ENTITY
    if not update_anime:
        return {"error": f"anime id {id} not found"}, HTTPStatus.NOT_FOUND

    serialized_anime = Animes.serialize_animes(updated_anime)

    
    if serialized_anime == []:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND
    return jsonify(serialized_anime), HTTPStatus.OK

def delete(id):
    animes = Animes.delete_anime(id)
    if not animes:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT