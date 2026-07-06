from pydantic import BaseModel


class TradeRouteResponse(BaseModel):
    origin: str
    destination: str
    resource: str
    amount: float
    profit: float


class TradeResultResponse(BaseModel):

    success: bool

    resource: str

    amount: float

    price: float

    total_cost: float

    buyer: str

    seller: str

    message: str