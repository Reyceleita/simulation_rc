"""
sleep.py
"""

from sim.core.City.location_registry import LocationType


def start(action, npc, world):

    world.logger.log(
        f"NPC {npc.id} se fue a dormir."
    )
    
    npc.current_location = \
        npc.city.locations[
            LocationType.RESIDENTIAL
        ]


def update(action, npc, world):

    npc.energy = min(
        100,
        npc.energy + 8
    )

    npc.stress = max(
        0,
        npc.stress - 2
    )

    npc.hunger += 0.5


def finish(action, npc, world):

    npc.memory.record_short(
        "slept"
    )

    world.logger.log(
        f"NPC {npc.id} despertó."
    )


