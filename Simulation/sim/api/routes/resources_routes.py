from typing import Dict, List, Optional

from fastapi import APIRouter, Query

from sim.api.models.resources_models import WorldResourcesResponse
from sim.api.dependences import (
    get_world,
)

router = APIRouter(
    tags=["Resources"]
)

@router.get(
    "/resources/global",
    response_model=WorldResourcesResponse,
    tags=["Recursos"],
    summary="Listar recursos del mundo",
    description="Retorna todos los recursos existentes en el mundo junto a su cantidad"
)
def global_resources():
    world = get_world()
    response = world.stats_tracker.resource_history
    
    return WorldResourcesResponse(
        resources=response
    )