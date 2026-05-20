from typing import Dict, List, Optional

from fastapi import APIRouter, Query

from sim.api.dependences import (
    get_world,
)
from sim.api.models.trade_models import TradeResultResponse, TradeRouteResponse

router = APIRouter(
    tags=["Comercio"]
)

@router.get(
    "/trade/routes",
    response_model=List[TradeRouteResponse],
    tags=["Comercio"],
    summary="Rutas comerciales activas",
    description="Lista las rutas comerciales vigentes entre ciudades con su rentabilidad.",
)
def get_trade_routes():
    world = get_world()
    routes = world.get_trade_routes()
    return [
        TradeRouteResponse(
            origin=r.origin.name,
            destination=r.destination.name,
            profit=r.profit,
        )
        for r in routes
    ]


@router.get(
    "/trade/classify",
    tags=["Comercio"],
    summary="Clasificar ciudades",
    description="Clasifica las ciudades en compradoras y vendedoras según su ratio comida/población.",
)
def classify_cities():
    world = get_world()
    buyers, sellers = world.trade_manager.classify_cities(world.cities)
    return {
        "buyers": [c.name for c in buyers],
        "sellers": [c.name for c in sellers],
    }


@router.post(
    "/trade/execute",
    response_model=List[TradeResultResponse],
    tags=["Comercio"],
    summary="Ejecutar comercio",
    description="Ejecuta manualmente todas las transacciones comerciales posibles entre ciudades.",
)
def execute_trade():
    world = get_world()
    results = world.trade_manager.trade_between_cities(world.cities)
    return [
        TradeResultResponse(
            success=r.success,
            amount=r.amount,
            price=r.price,
            total_cost=r.total_cost,
            message=r.message,
        )
        for r in results
    ]