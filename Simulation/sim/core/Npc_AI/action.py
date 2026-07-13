from dataclasses import dataclass, field
from sim.core.Npc_AI.action_types import ActionType


@dataclass(slots=True)

class Action:

    type: ActionType

    duration: int

    remaining: int

    elapsed: int = 0
    
    interruptible: bool = False

    data: dict = field(default_factory=dict)