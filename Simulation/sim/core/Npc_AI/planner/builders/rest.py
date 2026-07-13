from Simulation.sim.core.Npc_AI.action import Action
from Simulation.sim.core.Npc_AI.action_types import ActionType
from Simulation.sim.core.Npc_AI.planner.helpers.time_calculate import block_duration

def build(plan, npc, world, block, duration):

    plan.append(
        Action(
            type=ActionType.REST,
            duration=duration,
            remaining=duration,
            interruptible= True
        )
    )