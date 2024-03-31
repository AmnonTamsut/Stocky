import httpx
import requests
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import aiohttp
import asyncio

router = APIRouter()

base_url = "http://backend:4321"


@router.put("/new/", status_code=200)
def new_user(user_email: str, password: str):
    url = base_url + "/db/users/new"
    res = requests.put(url, params={"user_email": user_email, "password": password})
    return res.json()


@router.get("/connect/", status_code=200)
def new_user(user_email: str, password: str):
    url = base_url + "/db/login/"
    res = requests.get(url, params={"user_email": user_email, "password": password})
    return res.json()


@router.post("/stock/", status_code=200)
async def add_stock(unique_id, symbol):
    url = base_url + "/db/stocks/add/"
    NO_PROXY = {
        'no': 'pass',
    }

    res = requests.post(url, params={"unique_id": unique_id, "symbol": symbol}, proxies=NO_PROXY)
    return res.json()


@router.get("/", status_code=200)
async def add_stock(email: str):
    url = base_url + "/db/users/"
    res = requests.get(url, params={"email": email})
    async with httpx.AsyncClient() as cli:
        r = await cli.get(url)
    return r


@router.post("/s/", status_code=200)
async def add_stock(unique_id, symbol):
    url = base_url + "/db/stocks/add/"
    res = requests.post(url, params={"unique_id": unique_id, "symbol": symbol})
    return res.json()

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
