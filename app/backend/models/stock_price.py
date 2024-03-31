from pydantic import BaseModel


class StockPrice(BaseModel):
    symbol: str
    price: float
    market_cap: float
    timestamp: str
