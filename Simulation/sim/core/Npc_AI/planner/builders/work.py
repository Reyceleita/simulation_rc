from sim.core.Npc_AI.planner.helpers.time_calculate import block_duration
from sim.core.Npc_AI.action import Action
from sim.core.Npc_AI.action_types import ActionType


def build(plan, npc, world, block, duration):

    if npc.profession == "unemployed":
        return

    plan.append(
        Action(
            type=ActionType.WORK,
            duration=duration,
            remaining=duration,
            data={
                "job": npc.job
            }
        )
    )