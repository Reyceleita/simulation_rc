from typing import Dict, List

from fastapi import APIRouter, HTTPException

from sim.api.dependences import (
    get_world,
)
from sim.api.helpers.helpers import _city_to_response, _find_city
from sim.api.models.city_models import CityResponse, EmploymentStatsResponse
from sim.api.models.simulation_models import CityHistoryResponse
router = APIRouter(
    tags=["Cities"]
)

@router.get(
    "/cities",
    response_model=List[CityResponse],
    tags=["Ciudades"],
    summary="Listar ciudades",
    description="Retorna todas las ciudades con su estado completo: población, recursos, precios, empleo y métricas sociales.",
)
def list_cities():
    world = get_world()
    result = []
    for city in world.cities:
        social = city.social.calculate(city.npcs)
        employment = city.social.get_employment_stats(city.npcs)
        result.append(_city_to_response(city, social, employment))
    return result


@router.get(
    "/cities/{city_name}",
    response_model=CityResponse,
    tags=["Ciudades"],
    summary="Detalle de ciudad",
    description="Retorna el estado detallado de una ciudad por nombre.",
)
def get_city(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    social = city.social.calculate(city.npcs)
    employment = city.social.get_employment_stats(city.npcs)
    return _city_to_response(city, social, employment)


@router.get(
    "/cities/{city_name}/history",
    response_model=CityHistoryResponse,
    tags=["Ciudades"],
    summary="Historial de ciudad",
    description="Serie temporal de todas las métricas de una ciudad.",
)
def get_city_history(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    h = city.get_history()
    return CityHistoryResponse(
        food=h.get("food", []),
        population=h.get("population", []),
        employed=h.get("employed", []),
        unemployed=h.get("unemployed", []),
        prices=h.get("prices", []),
        hunger=h.get("hunger", []),
        money=h.get("money", []),
        stress=h.get("stress", []),
        happiness=h.get("happiness", []),
    )


@router.get(
    "/cities/{city_name}/history/{metric}",
    response_model=List[float],
    tags=["Ciudades"],
    summary="Historial de métrica específica",
    description=(
        "Retorna la serie temporal de una métrica individual de la ciudad. "
        "Métricas disponibles: food, population, employed, unemployed, prices, "
        "hunger, money, stress, happiness."
    ),
)
def get_city_metric_history(city_name: str, metric: str):
    world = get_world()
    city = _find_city(world, city_name)
    data = city.get_history(metric)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Métrica '{metric}' no encontrada.")
    return data


@router.get(
    "/cities/{city_name}/employment",
    response_model=EmploymentStatsResponse,
    tags=["Ciudades"],
    summary="Estadísticas de empleo",
    description="Cuenta de empleados y desempleados en la ciudad.",
)
def get_city_employment(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    stats = city.get_employment_stats()
    return EmploymentStatsResponse(**stats)


@router.get(
    "/cities/{city_name}/professions",
    response_model=Dict[str, int],
    tags=["Ciudades"],
    summary="Desglose de profesiones",
    description="Cantidad de NPCs por profesión en la ciudad.",
)
def get_city_professions(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.social.get_profession_breakdown(city.npcs)


@router.get(
    "/cities/{city_name}/resources",
    response_model=Dict[str, float],
    tags=["Ciudades"],
    summary="Recursos de la ciudad",
    description="Inventario de recursos (comida, bienes) de la ciudad.",
)
def get_city_resources(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.resources


@router.get(
    "/cities/{city_name}/prices",
    response_model=Dict[str, int],
    tags=["Ciudades"],
    summary="Precios actuales",
    description="Precios de mercado actuales de la ciudad.",
)
def get_city_prices(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.cost_of_life
