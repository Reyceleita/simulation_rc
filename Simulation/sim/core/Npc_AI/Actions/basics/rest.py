"""
rest.py
"""

def start(action, npc, world):

    world.logger.log(
        f"NPC {npc.id} comenzó a descansar."
    )


def update(action, npc, world):

    npc.energy = min(
        100,
        npc.energy + 4
    )

    npc.stress = max(
        0,
        npc.stress - 1
    )


def finish(action, npc, world):

    npc.memory.record_short(
        "rested"
    )

    world.logger.log(
        f"NPC {npc.id} terminó de descansar."
    )
