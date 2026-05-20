from dataclasses import dataclass
from typing import Dict


@dataclass
class DecisionSnapshot:
    tick: int
    npc_id: int

    chosen_action: str

    #evaluated_actions: Dict[str, float]

    hunger: float
    energy: float
    happiness: float
    stress: float

    reason: str