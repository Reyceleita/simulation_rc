from typing import List

from pydantic import BaseModel

from sim.api.api import GlobalStatsResponse
from sim.api.models.trade_models import TradeResultResponse


class TimeResponse(BaseModel):
    tick: int
    day: int
    hour: int
    time_string: str
    
class TickResponse(BaseModel):
    tick: int
    day: int
    hour: int
    trade_results: List[TradeResultResponse]
    global_stats: GlobalStatsResponse

class WorldHistoryResponse(BaseModel):
    money: List[float]
    hunger: List[float]
    happiness: List[float]
    stress: List[float]


class CityHistoryResponse(BaseModel):
    food: List[float]
    population: List[int]
    employed: List[int]
    unemployed: List[int]
    prices: List[int]
    hunger: List[float]
    money: List[float]
    stress: List[float]
    happiness: List[float]

class GlobalStatsResponse(BaseModel):
    total_npcs: int
    total_money: float
    avg_hunger: float
    avg_happiness: float
    avg_stress: float
    avg_money: float