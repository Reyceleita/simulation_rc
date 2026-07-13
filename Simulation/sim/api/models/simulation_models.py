from typing import List

from pydantic import BaseModel

from sim.api.models.trade_models import TradeResultResponse


class TimeResponse(BaseModel):
    tick: int
    day: int
    hour: int
    month : int
    year: int
    week_day : int
    week_day_name : str
    month_name : str
    time_string: str
    

class GlobalStatsResponse(BaseModel):

    # Población
    total_npcs: int

    # Economía NPCs
    total_money: float
    avg_money: float

    # Estado social
    avg_hunger: float
    avg_happiness: float
    avg_stress: float

    # Economía mundial
    total_market_value: float

    # Recursos globales por categoría
    total_food: float
    total_materials: float
    total_industrial: float
    total_consumer: float
    total_luxury: float
    total_energy: float
    total_illegal: float

class TickResponse(BaseModel):
    tick: int
    day: int
    hour: int
    trade_results: List[TradeResultResponse]
    global_stats: GlobalStatsResponse

class WorldHistoryResponse(BaseModel):

    # Estadísticas sociales
    money: List[float]
    hunger: List[float]
    happiness: List[float]
    stress: List[float]

    # Demografía
    population: List[int]

    # Economía
    total_market_value: List[float]

    # Recursos por categoría
    total_food: List[float]
    total_materials: List[float]
    total_industrial: List[float]
    total_consumer: List[float]
    total_luxury: List[float]
    total_energy: List[float]
    total_illegal: List[float]


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

