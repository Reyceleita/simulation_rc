from pydantic import BaseModel


class TradeRouteResponse(BaseModel):
    origin: str
    destination: str
    profit: float


class TradeResultResponse(BaseModel):
    success: bool
    amount: int
    price: float
    total_cost: float
    message: str