"""
socialize.py

Handler de la acción SOCIALIZE.
"""


# -------------------------------------------------------
# Inicio de la acción
# -------------------------------------------------------

from sim.core.City.location_registry import LocationType


def start(action, npc, world):
    """
    Busca un objetivo y comienza la interacción.
    """
    
    target = npc.social.choose_target(
        npc,
        world
    )
    
    if target is None:
    
        action.cancel()
    
        return
    
    action.data["target"] = target
    
    npc.current_location = \
        npc.city.locations[
            LocationType.RESIDENTIAL
        ]

# -------------------------------------------------------
# Tick de la acción
# -------------------------------------------------------

def update(action, npc, world):
    """
    Efectos mientras dura la conversación.
    """

    if action.data.get("cancelled"):
        return

    npc.energy -= 2

    npc.stress = max(
        0,
        npc.stress - 0.5
    )


# -------------------------------------------------------
# Final de la acción
# -------------------------------------------------------

def finish(action, npc, world):

    if action.data.get("cancelled"):
        return

    target = action.data["target"]

    result = npc.social.resolve_interaction(
        npc,
        target,
        world
    )

    world.logger.log(

        f"NPC {npc.id} terminó de hablar con NPC {target.id} "
        f"({result['type']}, "
        f"{result['relationship_change']:+.2f})"

    )

    world.busy_npcs.discard(npc.id)
    world.busy_npcs.discard(target.id)
