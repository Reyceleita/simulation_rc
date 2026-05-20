from typing import Dict, List, Optional

from fastapi import APIRouter, Query

from sim.api.dependences import (
    get_world,
)
from sim.api.helpers.helpers import _find_npc, _npc_to_response
from sim.api.models.npc_models import LatestDecisionsResponse, NPCDecisionItemResponse, NPCDecisionsResponse, NPCMemoryResponse, NPCRelationshipsResponse, NPCResponse
router = APIRouter(
    tags=["NPCs"]
)

@router.get(
    "/npcs",
    response_model=List[NPCResponse],
    tags=["NPCs"],
    summary="Listar NPCs",
    description="Lista todos los NPCs. Opcionalmente filtra por ciudad o profesión.",
)
def list_npcs(
    city: Optional[str] = Query(None, description="Filtrar por nombre de ciudad"),
    profession: Optional[str] = Query(None, description="Filtrar por profesión"),
    limit: int = Query(50, ge=1, le=500, description="Máximo de NPCs retornados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
):
    world = get_world()
    npcs = world.npcs

    if city:
        npcs = [n for n in npcs if n.city.name.lower() == city.lower()]
    if profession:
        npcs = [n for n in npcs if n.profession.lower() == profession.lower()]

    npcs = npcs[offset: offset + limit]
    return [_npc_to_response(n) for n in npcs]


@router.get(
    "/npcs/{npc_id}",
    response_model=NPCResponse,
    tags=["NPCs"],
    summary="Detalle de NPC",
    description="Retorna el estado completo de un NPC por ID.",
)
def get_npc(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return _npc_to_response(npc)

@router.get(
    "/decisions/latest",
    response_model=
        LatestDecisionsResponse,
    tags=["NPCs"],
    summary=
        "Últimas decisiones globales",
    description=
        "Retorna todas las decisiones "
        "tomadas por los NPCs "
        "durante el último tick.",
)
def get_latest_decisions():
    world = get_world()
    tick = world.time_manager.tick
    decisions = (
        world.decision_tracker
        .get_tick_decisions(tick)
    )
    parsed = [
        NPCDecisionItemResponse(
            npc_id=d.npc_id,
            chose_action=
                d.chosen_action,
            reason=d.reason,
            hunger=d.hunger,
            energy=d.energy,
            happiness=d.happiness,
            stress=d.stress,
        )
        
        for d in decisions
    ]
    return LatestDecisionsResponse(
        tick=tick,
        total_decisions=
            len(parsed),
        decisions=parsed,
    )

@router.get(
    "/npcs/{npc_id}/decisions",
    response_model=NPCDecisionsResponse,
    tags=["NPCs"],
    summary="Desicion del npc",
    description="Retorna la ultima desición tomada por el NPC junto a sus stats",
)
def get_npc_decision(npc_id: int):
    world = get_world()
    response = world.decision_tracker.get_latest(npc_id)
    return NPCDecisionsResponse(
        tick= response.tick,
        chose_action= response.chosen_action,
        energy= response.energy,
        happiness= response.happiness,
        hunger= response.hunger,
        npc_id= response.npc_id,
        reason= response.reason,
        stress= response.stress
    )

@router.get(
    "/npcs/{npc_id}/memory",
    response_model=NPCMemoryResponse,
    tags=["NPCs"],
    summary="Memoria del NPC",
    description="Retorna contadores de memoria a corto plazo y satisfacciones emocionales.",
)
def get_npc_memory(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return NPCMemoryResponse(
        memory_short=dict(npc.memory.memory_short),
        memory_emotional=dict(npc.memory.memory_emotional),
    )


@router.get(
    "/npcs/{npc_id}/relationships",
    response_model=NPCRelationshipsResponse,
    tags=["NPCs"],
    summary="Relaciones sociales del NPC",
    description="Retorna el mapa de relaciones del NPC con otros NPCs (valores en [-1, 1]).",
)
def get_npc_relationships(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return NPCRelationshipsResponse(
        npc_id=npc_id,
        relationships=dict(npc.social.relationships),
        average_relationship=npc.social.average_relationship(),
    )


@router.get(
    "/npcs/{npc_id}/history",
    response_model=Dict[str, List[float]],
    tags=["NPCs"],
    summary="Historial del NPC",
    description="Serie temporal de estadísticas del NPC (dinero, hambre, felicidad, estrés).",
)
def get_npc_history(npc_id: int):
    world = get_world()
    _find_npc(world, npc_id)  # Valida existencia
    return world.get_npc_history(npc_id)