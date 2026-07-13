from Simulation.sim.core.Npc_AI.action import Action
from Simulation.sim.core.Npc_AI.action_types import ActionType


def build(context):

    npc = context.npc

    plan = context.plan

    if npc.hunger > 70:

        plan.append(
            Action(
                ActionType.BUY,
                duration=1
            )
        )

        plan.append(
            Action(
                ActionType.EAT,
                duration=1
            )
        )

        return

    if npc.energy < 30:

        plan.append(
            Action(
                ActionType.REST,
                duration=2
            )
        )

        return

    if npc.social.average_relationship() > 30:

        plan.append(
            Action(
                ActionType.SOCIALIZE,
                duration=2
            )
        )

        return

    plan.append(
        Action(
            ActionType.WANDER,
            duration=2
        )
    )