from typing import Dict, List, Optional

from pydantic import BaseModel


class NPCDecisionsResponse(BaseModel):
    tick: int
    npc_id: int
    chose_action: str
    hunger: float
    energy: float
    happiness: float
    stress: float
    reason: str

class NPCDecisionItemResponse(BaseModel):
    npc_id: int
    chose_action: str
    reason: str
    hunger: float
    energy: float
    happiness: float
    stress: float


class LatestDecisionsResponse(BaseModel):
    tick: int
    total_decisions: int
    decisions: List[
        NPCDecisionItemResponse
    ]

class NPCPersonalityResponse(BaseModel):
    greed: float
    sociability: float
    risk: float
    discipline: float
    empathy: float
    impulsiveness: float


class NPCInventoryResponse(BaseModel):
    food: int
    goods: int


class NPCResponse(BaseModel):
    id: int
    profession: str
    city: str
    money: float
    hunger: float
    energy: float
    happiness: float
    stress: float
    satiety: float
    metabolism: float
    hunger_threshold: int
    personality: NPCPersonalityResponse
    inventory: NPCInventoryResponse
    trade_route: Optional[str]


class NPCMemoryResponse(BaseModel):
    memory_short: Dict[str, float]
    memory_emotional: Dict[str, float]


class NPCRelationshipsResponse(BaseModel):
    npc_id: int
    relationships: Dict[int, float]
    average_relationship: float