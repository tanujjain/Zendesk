from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from components.track_order import OrderTracking
from components.cancel_order import OrderCancellation


app = FastAPI()

@app.get("/")
def read_root() -> Dict:
    return {"Hello": "World"}

class ConvHistory(BaseModel):
    message_history: List[Dict[str, str]]

class TrackOrderResponse(BaseModel):
    response: str

class CancelOrderResponse(BaseModel):
    response: str


@app.post("/track_order")
async def track_order(conv_history: ConvHistory) -> TrackOrderResponse:
    order_tracker = OrderTracking()
    res = await order_tracker(conv_history.message_history)
    return TrackOrderResponse(response=res)


@app.post("/cancel_order")
async def cancel_order(conv_history: ConvHistory) -> CancelOrderResponse:
    order_canceller = OrderCancellation()
    res = await order_canceller(conv_history.message_history)
    return CancelOrderResponse(response=res)