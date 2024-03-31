from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.stock_alerts import StockAlert
from pymongo import MongoClient

router = APIRouter()

client = MongoClient("localhost", 27017)
db = client.alerts

alerts = db.alerts


@router.post("/create/", status_code=201)
async def create_stock_alert(alert: StockAlert):
    result = alerts.insert_one({"symbol": alert.symbol,
                                "price_threshold": alert.price_threshold,
                                "active": alert.active
                                })
    return {"id": str(result.inserted_id)}


@router.get("/{alert_id}", response_model=StockAlert, status_code=200)
async def get_stock_alert(alert_id: str):
    alert = alerts.find_one({"_id": ObjectId(alert_id)})
    if alert:
        return alert
    else:
        raise HTTPException(status_code=404, detail="Stock alert not found")


@router.delete("/{alert_id}", status_code=200)
async def delete_alert(alert_id):
    if alerts.find_one({"_id": ObjectId(alert_id)}):
        found = alerts.find_one({"_id": ObjectId(alert_id)})
        result = alerts.delete_one(found)
        if result.raw_result['n'] >= 1:
            return {"message", "Stock alert deleted"}
        else:
            raise HTTPException(status_code=404, detail="Stock alert not found")

