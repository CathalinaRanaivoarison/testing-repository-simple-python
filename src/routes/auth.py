import json

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token

from src.static import DATA_FILE_PATH

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.post("/authenticate")
def authenticate():
    try:
        username = request.form["username"]
    except KeyError:
        return jsonify(
            {
                "name": "Bad Request",
                "msg": "Need username to be authenticated.",
                "solution": "Try again.",
                "status_code": 400,
            }
        )

    with open(DATA_FILE_PATH, encoding="utf-8", mode="w+") as data_file:
        try:
            data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            data = {"users": []}

        try:
            id = data["users"].index(username)
        except ValueError:
            id = len(data["users"])

        identity = {
            "id": id,
            "username": username,
        }

        access_token = create_access_token(
            identity=identity, fresh=True, additional_claims={}
        )

        response = {"success": True, "return": {"access": access_token}, "code": 200}

        resp = jsonify(response)

        data["users"].append(username)
        json.dump(data, data_file, ensure_ascii=False, indent=4)

        return resp
