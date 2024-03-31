from pydantic import BaseModel


class StockAlert(BaseModel):
    symbol: str
    price_threshold: float
    active: bool
