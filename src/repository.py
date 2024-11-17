from datetime import datetime
from sqlalchemy import text
from src.database import db

# delete user from SQL database
def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id = :id")
    db.session.execute(sql, {
        "id": user_id,
        })
    db.session.commit()
    return "Successfully deleted user!"

    
def check_username(username):
    sql = text("SELECT id FROM users WHERE username = :username LIMIT 1")
    result = db.session.execute(sql, {"username": username})

    user = result.fetchone()

    if user is not None:
        return user.id
    else:
        return None


def insert_account(fullname, username, hash_password):
    sql = text(
        "insert into users (fullname, username, password, created_at, updated_at) values (:fullname, :username, :password, :created_at, :updated_at)"
    )
    db.session.execute(
        sql,
        {
            "fullname": fullname,
            "username": username,
            "password": hash_password,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
    )
    db.session.commit()

    return "Successfully created account!"


def get_hashed_password(username):
    sql = text("SELECT password FROM users WHERE username = :username LIMIT 1")
    result = db.session.execute(sql, {"username": username})

    row = result.fetchone()

    return row[0] if row else None


def get_fullname(user_id):
    sql = text("SELECT fullname FROM users WHERE id = :id LIMIT 1")
    result = db.session.execute(sql, {"id": user_id})

    row = result.fetchone()

    return row[0] if row else None