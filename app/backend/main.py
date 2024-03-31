import uvicorn
from fastapi import FastAPI
from routers import users, stock_price
from routers import db

app = FastAPI()
app.include_router(stock_price.router, prefix="/stock", tags=["stock"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(db.router, prefix="/db", tags=["db"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=4321)
