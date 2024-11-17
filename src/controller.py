from flask import jsonify, make_response
from src.service import RegisterModel, Loginmodel, DeleteUserModel
from src.repository import check_username, insert_account, get_fullname
from src.helper import generate_jwt
from src.variable import EXPIRES
from src.helper import decode_jwt

def delete_controller(request_json):
    username = request_json.get("username")
    password = request_json.get("password")

    # delete user from database
    deleted_user = DeleteUserModel(username, password)

    # validate request JSON
    isValid, message = deleted_user.validation(password)
    # response error
    if not isValid:
        return jsonify({"status_code": 400, "message": message["error"]}), 400

    # response success
    success_message = (
        jsonify({"status_code": 200, "message": message}),
        200,
    )
    response = make_response(success_message)

    return response


def register_controller(request_json):
    fullname = request_json.get("fullname")
    username = request_json.get("username")
    password = request_json.get("password")

    user = RegisterModel(fullname, username, password)

    # validate request JSON
    valid, error_message = user.validate()
    if not valid:
        return jsonify({"status_code": 400, "message": error_message["error"]}), 400

    # check username exist
    user_exist = check_username(username)
    if user_exist:
        return jsonify({"status_code": 400, "message": "Username already exist!"}), 400

    # hash password
    hash_password = user.hash_password()

    # insert user data to database
    success_message = insert_account(fullname, username, hash_password)

    # response success
    success_message = (
        jsonify({"status_code": 201, "message": success_message}),
        200,
    )
    response = make_response(success_message)

    return response


def login_controller(request_json):
    username = request_json.get("username")
    password = request_json.get("password")

    login = Loginmodel(username, password)

    # validate request JSON
    valid, error_message = login.validate()
    if not valid:
        return jsonify({"status-code": 400, "message": error_message["error"]}), 400

    # check username exist returning user id
    user = check_username(username)
    if not user:
        return jsonify(
            {"status_code": 400, "message": "Username or Password is wrong!"}
        ), 400

    # verify password
    valid = login.check_password(password)
    if not valid:
        return jsonify(
            {"status_code": 400, "message": "Username or password is wrong!"}
        ), 400

    # create session token (cookies + jwt)
    token = generate_jwt(user)

    # response successs
    success_message = (
        jsonify({"status_code": 200, "message": "Login successfully!"}),
        200,
    )
    response = make_response(success_message)

    # set cookie
    response.set_cookie(
        "X-LIVENESS-TOKEN", token, httponly=True, samesite="lax", expires=EXPIRES
    )

    return response


def logout_controller():
    response = make_response(
        jsonify({"status_code": 200, "message": "Logged out"}), 200
    )

    # Clear the JWT cookie
    response.set_cookie("X-LIVENESS-TOKEN", "", expires=0)

    return response


def main_controller():
    response = {"status_code": 200, "message": "You found me!"}
    return jsonify(response), 200


def home_controller(token):
    # decode token
    user_id = decode_jwt(token)

    # get username
    fullname = get_fullname(user_id)

    response = (
        jsonify({"status_code": 200, "message": f"Hello {fullname}"}),
        200,
    )
    return response