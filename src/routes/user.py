import json

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

from src.static import DATA_FILE_PATH
from src.utils.misc import capitalize_name

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/id")
@jwt_required()
def get_user_id():
    with open(DATA_FILE_PATH, encoding="utf-8", mode="r") as data_file:
        data = json.load(data_file)

        try:
            return f"Your id is : {data['users'].index(current_user['username'])}", 200
        except ValueError:
            return jsonify(
                {
                    "name": "Bad Request",
                    "msg": "This username is already used.",
                    "solution": "Try again.",
                    "status_code": 400,
                }
            )


@user_bp.route("/hello")
@jwt_required()
def get_hello():
    return f"Hello {capitalize_name(current_user['username'])}"
