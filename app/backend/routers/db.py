import re
from datetime import datetime
from typing import List

import bcrypt
import requests
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")

router = APIRouter()

db_users = client.users
db_stocks = client.stocks
db_alerts = client.alerts

users = db_users.users
stocks = db_stocks.stocks
alerts = db_alerts.alerts

users.drop()
stocks.drop()

class Stock(BaseModel):
    name: str
    symbol: str
    price: float


class Stocks(BaseModel):
    table: List[Stock] = []
    time: str


class Index(BaseModel):
    table: List[Stock] = []
    time: str


def is_email_registered(user_email):
    if users.find_one({"email": user_email}):
        return True
    return False


def one_min_passed(time_one: datetime, time_two: datetime):
    res = time_two - time_one
    sec = res.total_seconds()
    one_min = 60
    return sec > one_min


@router.put("/users/new", status_code=200)
def db_insert(user_email: str, password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    if not is_email_registered(user_email):
        result = users.insert_one({"email": user_email,
                                   "password": hashed,
                                   "stocks": []})
        return {"id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=409, detail="Email is used by another user")


# sample data

stocks.insert_one({
  "table": [
    {
      "name": "Microsoft Corporation",
      "symbol": "MSFT",
      "price": 420.7200012207031
    },
  ],
  "time": "01/03/2024, 00:13:49"
})
##############

@router.get("/users", status_code=200)
async def get_user(user_email: str):
    user = users.find_one({"email": user_email})
    if user:
        return {"email": user['email'], "password": user["password"], "stocks": user["stocks"]}
    return {"no user found"}


@router.get("/id/{user_email}", status_code=200)
async def get_user_id(unique_id):
    check_for_hex_regexp = re.compile(r"^[0-9a-fA-F]{24}$")
    if check_for_hex_regexp.match(unique_id):
        user = users.find_one({"_id": ObjectId(unique_id)})
        if user:
            return {"email": user['email'], "password": user["password"], "stocks": user["stocks"]}
    return {"no user found"}


@router.get("/login/", status_code=200)
async def login(user_email, password):
    encoding = 'utf-8'
    hashed_password = users.find_one({"email": user_email})["password"]
    res = bcrypt.checkpw(bytes(password, encoding), hashed_password)
    return {"login": res}


@router.post("/stocks/add/", status_code=200)
async def add_stock(unique_id, symbol):
    check_for_hex_regexp = re.compile(r"^[0-9a-fA-F]{24}$")

    if check_for_hex_regexp.match(unique_id):

        result = users.update_one({"_id": ObjectId(unique_id)},
                                  {"$addToSet": {"stocks": symbol.upper()}})
        if result.raw_result['nModified'] >= 1.0:
            return {"details": "stock added successfully"}
        return {"details": "stock already added"}

    else:
        raise HTTPException(status_code=400, detail="invalid id")


@router.get("/index/snp500")
async def snp500():
    now = datetime.now()

    document = stocks.find_one()
    return {"table": document["table"], "time": document["time"]}


@router.post("/index/snp500", status_code=200)
async def snp500(data: Stocks):
    stocks.drop()
    table = []
    for i in data.table:
        table.append({"name": i.name, "symbol": i.symbol, "price": i.price})
    res = stocks.insert_one({"table": table, "time": data.time})
    return {"result": res.acknowledged}


@router.get("/users/all", status_code=200)
async def get_users():
    all_users = []
    for user in users.find():
        all_users.append(
            {"_id": str(user["_id"]), "email": user["email"], "password": user["password"], "stocks": user["stocks"]})
    return all_users


@router.delete("/stock/delete", status_code=200)
async def delete_from_my_stocks(user_id: str, symbol: str):
    u = users.find_one({"_id": ObjectId(user_id)})

    if symbol in u["stocks"]:
        filter_query = {"_id": ObjectId(user_id)}
        update_query = {"$pull": {"stocks": symbol}}
        users.update_one(filter_query, update_query)

    return {"result": u["stocks"]}



