from sim.core.Npc_AI.action import Action
from sim.core.Npc_AI.action_types import ActionType

def build(plan, npc, world, block, duration):

    plan.append(
        Action(
            type=ActionType.EAT,
            duration=duration,
            remaining=duration,
        )
    )