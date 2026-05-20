from fastapi import HTTPException

from sim.api.models.city_models import CityResponse, EmploymentStatsResponse, SocialMetricsResponse
from sim.api.models.npc_models import NPCInventoryResponse, NPCPersonalityResponse, NPCResponse


def _find_city(world, name: str):
    for city in world.cities:
        if city.name.lower() == name.lower():
            return city
    raise HTTPException(status_code=404, detail=f"Ciudad '{name}' no encontrada.")


def _find_npc(world, npc_id: int):
    for npc in world.npcs:
        if npc.id == npc_id:
            return npc
    raise HTTPException(status_code=404, detail=f"NPC con id={npc_id} no encontrado.")


def _city_to_response(city, social, employment) -> CityResponse:
    return CityResponse(
        name=city.name,
        type=city.type,
        culture=city.culture,
        base_stress=city.base_stress,
        population=len(city.npcs),
        treasury=city.treasury,
        resources=city.resources,
        prices=city.cost_of_life,
        employment=EmploymentStatsResponse(**employment),
        social_metrics=SocialMetricsResponse(
            avg_hunger=social.avg_hunger,
            avg_money=social.avg_money,
            avg_stress=social.avg_stress,
            avg_happiness=social.avg_happiness,
            wellbeing_index=social.wellbeing_index,
        ),
    )


def _npc_to_response(npc) -> NPCResponse:
    trade_route_str = None
    if npc.trade_route:
        tr = npc.trade_route
        if isinstance(tr, dict):
            trade_route_str = f"{tr.get('from', {}).get('name', '?')} → {tr.get('to', {}).get('name', '?')}"
        else:
            trade_route_str = f"{tr.origin.name} → {tr.destination.name}"

    return NPCResponse(
        id=npc.id,
        profession=npc.profession,
        city=npc.city.name if npc.city else "sin ciudad",
        money=npc.money,
        hunger=npc.hunger,
        energy=npc.energy,
        happiness=npc.happiness,
        stress=npc.stress,
        satiety=npc.satiety,
        metabolism=npc.metabolism,
        hunger_threshold=npc.hunger_threshold,
        personality=NPCPersonalityResponse(**npc.personality),
        inventory=NPCInventoryResponse(**npc.inventory),
        trade_route=trade_route_str,
    )