from flask import jsonify, request, Blueprint
from src.controller import (
    login_controller,
    register_controller,
    logout_controller,
    main_controller,
    home_controller,
    delete_controller,
)

bp = Blueprint("main", __name__)


@bp.route("/auth/register", methods=["POST"])
def register():
    request_json = request.get_json()
    return register_controller(request_json)

@bp.route("/auth/login", methods=["POST"])
def login():
    request_json = request.get_json()
    return login_controller(request_json)


@bp.route("/auth/logout", methods=["DELETE"])
def logout():
    return logout_controller()

@bp.route("/auth/delete", methods=["DELETE"])
def delete():
    request_json = request.get_json()
    return delete_controller(request_json)


@bp.route("/", methods=["GET"])
def main():
    return main_controller()

@bp.route("/home", methods=["GET"])
def home():
    token = request.cookies.get("X-LIVENESS-TOKEN")
    if not token:
        unauthorized_message = {"status_code": 401, "message": "Unauthorized users"}
        return jsonify(unauthorized_message), 401

    return home_controller(token)