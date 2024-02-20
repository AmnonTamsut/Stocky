from fastapi import FastAPI
from stock_price_retrieval import *
app = FastAPI()


@app.get('/')
async def root():
    return {'example': 'This is an example', 'data': 0}


@app.get('/login')
async def login():
    return {'login.py': 'This is login.py', 'data': 1}


@app.get('/dashboard')
async def dashboard():
    return {'dashboard': 'This is dashboard', 'data': 2}


@app.get('/api/stock/{stock}')
async def api(stock: str):
    return get_data(stock)
