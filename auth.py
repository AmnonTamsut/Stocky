import bcrypt
import db


def login(email, password):
    encoding = 'utf-8'
    hashed_password = db.get_user(email)["password"]
    return bcrypt.checkpw(bytes(password, encoding), hashed_password)


