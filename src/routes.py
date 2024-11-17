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

@bp.route("/", methods=["GET"])
def main():
    """Render the main page.

    Returns:
        200: A message indicating the main endpoint has been accessed.
    """
    return main_controller()

@bp.route("/home", methods=["GET"])
def home():
    """Render the home page, requires X-LIVENESS-TOKEN as a cookie.

    Returns:
        401: Unauthorized users if token is not provided.
        200: Greeting message with user's fullname if token is valid.
    """
    token = request.cookies.get("X-LIVENESS-TOKEN")
    if not token:
        unauthorized_message = {"status_code": 401, "message": "Unauthorized users"}
        return jsonify(unauthorized_message), 401

    return home_controller(token)

@bp.route("/auth/register", methods=["POST"])
def register():
    """Register a new account with provided user details.

    Expects:
        POST request with JSON body containing 'fullname', 'username', and 'password'.

    Returns:
        400: If validation fails or username already exists.
        201: If registration is successful.
    """
    request_json = request.get_json()
    return register_controller(request_json)

@bp.route("/auth/login", methods=["POST"])
def login():
    """Authenticate user credentials and initiate a session.

    Expects:
        POST request with JSON body containing 'username' and 'password'.

    Returns:
        400: If validation fails or credentials are incorrect.
        200: If login is successful, sets a session token as a cookie.
    """
    request_json = request.get_json()
    return login_controller(request_json)


@bp.route("/auth/logout", methods=["DELETE"])
def logout():
    """Logout the current user, requires X-LIVENESS-TOKEN as a cookie.

    Returns:
        200: Logged out
    """
    return logout_controller()

@bp.route("/user/delete", methods=["DELETE"])
def delete():
    """Delete account, requires X-LIVENESS-TOKEN as a cookie.

    Returns:
        401: Unauthorized users
        200: Successfully deleted user!
    """
    token = request.cookies.get("X-LIVENESS-TOKEN")
    if not token:
        unauthorized_message = {"status_code": 401, "message": "Unauthorized users"}
        return jsonify(unauthorized_message), 401
    return delete_controller(token)