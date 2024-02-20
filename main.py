from fastapi import FastAPI
from stock_price_retrieval import *
import db
import auth
app = FastAPI()


@app.get('/')
async def root():
    return {'example': 'This is an example', 'data': 0}


@app.get('/login')
async def login(email: str, password: str):
    return auth.login(email,password)


@app.get('/dashboard')
async def dashboard():
    return {'dashboard': 'This is dashboard', 'data': 2}


@app.get('/api/stock')
async def api(stock: str):
    return get_data(stock)

@app.get('/api/stocks')
async def api(stocks: str, start: str, end: str):
    return get_multiple_data(stocks, start, end)