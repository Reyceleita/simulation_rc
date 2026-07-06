from ast import Dict
from typing import List

from pydantic import BaseModel


class ResourceResponse(BaseModel):
    name: str
    amount: float
    category: str
    market_value: float
    
class CityResourcesResponse(BaseModel):
    city_name: str
    total_market_value: float
    resources: List[ResourceResponse]

class CityResourceSummaryResponse(BaseModel):
    city_name: str

    population: int

    market_value: float

    total_food: float

    total_materials: float

    total_industrial: float

    total_consumer: float

    total_luxury: float

    total_energy: float

    total_illegal: float
    

class WorldResourcesResponse(BaseModel):
    resources: Dict[str, float]

    total_market_value: float

class ResourceHistoryResponse(BaseModel):
    resource: str
    history: List[float]

class CityHistoryResponse(BaseModel):

    city_name: str

    market_value: List[float]

    population: List[int]

    food: List[float]

    materials: List[float]

    industrial: List[float]

    consumer: List[float]

    luxury: List[float]

    energy: List[float]

    illegal: List[float]

class WorldStatsResponse(BaseModel):

    population: int

    avg_money: float

    avg_hunger: float

    avg_happiness: float

    avg_stress: float

    total_market_value: float

class WorldStatsHistoryResponse(BaseModel):

    money: List[float]

    hunger: List[float]

    happiness: List[float]

    stress: List[float]

    market_value: List[float]

    population: List[int]