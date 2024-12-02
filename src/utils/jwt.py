import json
from typing import Dict

from flask import jsonify
from flask_jwt_extended import JWTManager

from src.static import DATA_FILE_PATH


def register_jwt_handlers(jwt: JWTManager):
    @jwt.user_lookup_loader  # type: ignore
    def user_lookup_loader(
        _jwt_header: Dict[str, str], jwt_data: Dict[str, Dict[str, str]]
    ):
        identity = jwt_data["sub"]
        with open(DATA_FILE_PATH, encoding="utf-8", mode="r") as data_file:
            try:
                data = json.load(data_file)
            except json.decoder.JSONDecodeError:
                return None

            if data["users"][identity["id"]] != identity["username"]:
                return None
        return identity

    @jwt.expired_token_loader
    def expired_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token has expired.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.invalid_token_loader
    def invalid_token_loader(reason):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": f"Token is invalid: {reason}.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Fresh token is needed.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.revoked_token_loader
    def revoked_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token is revoked.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.unauthorized_loader
    def unauthorized_loader(reason):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": f"Unauthorized: {reason}.",
                "solution": "Check your parameters.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.token_verification_failed_loader
    def token_verification_failed_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token verification failed.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.user_lookup_error_loader
    def user_lookup_error_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "BadRequestError",
                "name": "BadRequest Error",
                "message": "User in identity not found in database.",
                "solution": "Try again.",
            },
            "code": 404,
            "status_code": 404,
        }
        return jsonify(json)
