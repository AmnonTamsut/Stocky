from datetime import datetime
from typing import List

import yfinance as yf
from fastapi import APIRouter
import httpx
from pydantic import BaseModel

from models.stock_price import StockPrice

router = APIRouter()


class Stock(BaseModel):
    name: str
    symbol: str
    price: float


class Stocks(BaseModel):
    table: List[Stock] = []
    time: str


@router.get("/{symbol}", response_model=StockPrice)
async def get_stock_price(symbol: str):
    stock_data = yf.Ticker(symbol).fast_info
    price = stock_data.last_price
    market_cap = stock_data.market_cap
    if not market_cap:
        market_cap = 0
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
    return {"symbol": symbol, "price": price, "market_cap": market_cap, "timestamp": timestamp}



@router.get("/index/snp500/latest/", status_code=200)
async def snp_latest():
    table_info = []

    # hard coding snp500 top10 companies due to API free tier limits
    tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META",
               "GOOGL", "GOOG", "BRK-B", "LLY", "AVGO"]

    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
    full_url = f"http://backend:4321" + f"/db/index/snp500"
    # res = requests.get(full_url)
    async with httpx.AsyncClient() as client:
        r = await client.get(full_url)
    if r:
        data = r.json()
        if not one_min_passed(datetime.strptime(data["time"], "%d/%m/%Y, %H:%M:%S"), now):
            return {"table": data["table"], "time": data["time"]}

    count = 0
    for s in tickers:
        ticker = yf.Ticker(s)
        count = count + 1
        name = ticker.info['longName']
        info = ticker.fast_info
        table_info.append({"name": name,
                           "symbol": s,
                           "price": info.last_price})
    data = Stocks(table=table_info, time=timestamp)

    print("-----------------------------")
    print()
    print(timestamp)
    print()
    print("-----------------------------")
    # updating cache to comply with yFinance API limits
    async with httpx.AsyncClient() as client:
        update_db_request = await client.post(full_url, json=data.dict(),
                                              headers={"Content-Type": "application/json"})
    return data



@router.get("/index/snp500/test", status_code=200)
async def snp_latest():
    table_info = []

    # hard coding snp500 top10 companies due to API free tier limits
    tickers = ["MSFT", "AAPL", "NVDA", "AMZN", "META",
               "GOOGL", "GOOG", "BRK-B", "LLY", "AVGO"]

    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
    full_url = f"http://backend:4321" + f"/db/index/snp500"
    for s in tickers:
        ticker = yf.Ticker(s)
        name = ticker.info['longName']
        info = ticker.fast_info
        table_info.append({"name": name,
                           "symbol": s,
                           "price": info.last_price})
    data = Stocks(table=table_info, time=timestamp)


    # updating cache to comply with yFinance API limits
    async with httpx.AsyncClient() as client:
        update_db_request = await client.post(full_url, json=data.dict(),
                                              headers={"Content-Type": "application/json"})
    return data




@router.get("/news/{symbol}")
async def get_stock_price(symbol: str):
    url = "https://api.tickertick.com/feed?q=z:"
    async with httpx.AsyncClient() as client:
        r = await client.get(url + symbol + "&n=10")
        return r.json()


def one_min_passed(time_one: datetime, time_two: datetime):
    res = time_two - time_one
    sec = res.total_seconds()
    one_min = 60
    return sec > one_min



