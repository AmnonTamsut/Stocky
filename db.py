from bson import ObjectId
from pymongo import MongoClient
import bcrypt

client = MongoClient("localhost", 27017)
db = client.users

users = db.users


def new_user(user_email, password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    users.insert_one({"email": user_email, "password": hashed, "stocks": []})
    a = 7


def get_user(email):
    return users.find_one({"email": email})


def get_user_id(unique_id):
    return users.find_one({"_id": ObjectId(unique_id)})


def add_stock(unique_id, symbol):
    users.update_one({"_id": ObjectId(unique_id)}, {"$addToSet": {"stocks": symbol}})
    print("success")


def is_email_registered(email):
    if users.find_one({"email": email}):
        return True
    return False


#add_stock("65d6143a8058aad7f3099819", "aapl")
# new_user("a","1234")
for p in users.find():
    print(p)
    #users.delete_one(p)
