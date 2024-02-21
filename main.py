from fastapi import FastAPI, HTTPException
import db
from stock_price_retrieval import *
import auth
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get('/')
async def root():
    return {'example': 'This is an example', 'data': 0}


@app.get('/login')
async def login(email: str, password: str):
    if auth.login(email, password):
        response = RedirectResponse(url="/dashboard")
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get('/dashboard')
async def dashboard():
    return {'yochay': 'hachatich', 'matay?': "tamid"}


@app.get('/api/stock')
async def api(stock: str):
    return get_data(stock)


@app.get('/api/stocks')
async def api(stocks: str, start: str, end: str):
    return get_multiple_data(stocks, start, end)


@app.put('/updatemystocks')
async def update_stocks(unique_id: str, symbol: str):
    try:
        db.add_stock(unique_id, symbol)
        return {"message": "Stock added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


