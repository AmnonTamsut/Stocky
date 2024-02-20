from pymongo import MongoClient
import bcrypt

client = MongoClient("localhost", 27017)
db = client.users

users = db.users


def new_user(email, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    users.insert_one({"email": email, "password": hashed})


def get_user(email):
    return users.find_one({"email": email})


def is_email_registered(email):
    if users.find_one({"email": email}):
        return True
    return False


# new_user("a", "8543851")


for p in users.find():
    print(p)
