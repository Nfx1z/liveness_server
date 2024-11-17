import bcrypt
from src.repository import get_hashed_password, check_username, delete_user

# delete user from SQL database
class DeleteUserModel:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # check username and password input
    def validation(self, password):
        errors = {}
        
        # check if username and password is empty
        if not self.username or not self.password:
            errors["error"] = "Username and Password is required!"
            return False, errors

        # check username in database
        user_id= check_username(self.username)
        if check_username(self.username) == None:
            errors["error"] = "Username not found!"
            return False, errors

        # check password
        bytes_pass = password.encode("utf-8")
        # retrieve hashed password from database
        hash_password = get_hashed_password(self.username)
        # convert hashed password to bytes
        bytes_hash_pass = hash_password.encode("utf-8")
        # compaard the input password with the password in database
        if not bcrypt.checkpw(bytes_pass, bytes_hash_pass):
            errors["error"] = "Password is incorrect!"
            return False, errors
        
        return True, delete_user((user_id))
        
class RegisterModel:
    MIN_INPUT_LENGTH = 5

    def __init__(self, fullname, username, password):
        self.fullname = fullname
        self.username = username
        self.password = password

    def validate(self):
        errors = {}

        if not self.fullname or not self.username or not self.password:
            errors["error"] = "Fullname, Username, and Password is required"

        if errors:
            return False, errors

        if (
            len(self.username) < self.MIN_INPUT_LENGTH
            or len(self.password) < self.MIN_INPUT_LENGTH
            or len(self.fullname) < self.MIN_INPUT_LENGTH
        ):
            errors["error"] = (
                f"Fullname, Username, and Password at least {self.MIN_INPUT_LENGTH} characters"
            )

        isValid = len(errors) == 0
        return isValid, errors

    def hash_password(self):
        password_bytes = self.password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes


class Loginmodel:
    MIN_INPUT_LENGTH = 5

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate(self):
        errors = {}

        if not self.username or not self.password:
            errors["error"] = "Username and Password is required"

        if errors:
            return False, errors

        if (
            len(self.username) < self.MIN_INPUT_LENGTH
            or len(self.password) < self.MIN_INPUT_LENGTH
        ):
            errors["error"] = (
                f"Username or Password at least {self.MIN_INPUT_LENGTH} characters"
            )

        isValid = len(errors) == 0
        return isValid, errors

    def check_password(self, password):
        bytes_pass = password.encode("utf-8")

        hash_password = get_hashed_password(self.username)
        bytes_hash_pass = hash_password.encode("utf-8")

        if bcrypt.checkpw(bytes_pass, bytes_hash_pass):
            return True
        return False