from typing import Dict

from pydantic import BaseModel


class SocialMetricsResponse(BaseModel):
    avg_hunger: float
    avg_money: float
    avg_stress: float
    avg_happiness: float
    wellbeing_index: float


class EmploymentStatsResponse(BaseModel):
    employed: int
    unemployed: int


class CityResourcesResponse(BaseModel):
    food: float


class CityPricesResponse(BaseModel):
    food_price: int


class CityResponse(BaseModel):
    name: str
    type: str
    culture: Dict[str, float]
    base_stress: float
    population: int
    treasury: float
    resources: Dict[str, float]
    prices: Dict[str, int]
    employment: EmploymentStatsResponse
    social_metrics: SocialMetricsResponse