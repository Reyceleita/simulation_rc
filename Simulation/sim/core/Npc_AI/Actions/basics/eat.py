"""
eat.py

Handler de la acción EAT.
"""

from sim.core.City.location_registry import LocationType
from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import ResourceCategory


# -------------------------------------------------------
# Inicio
# -------------------------------------------------------

def start(action, npc, world):
    """
    Selecciona la mejor comida del inventario.
    """

    best_food = None
    best_nutrition = -1

    for resource_name, amount in npc.inventory.items():

        if amount <= 0:
            continue

        definition = RESOURCES.get(resource_name)

        if definition is None:
            continue

        if definition.category != ResourceCategory.FOOD:
            continue

        if definition.nutrition > best_nutrition:

            best_food = resource_name
            best_nutrition = definition.nutrition

    if best_food is None:

        action.data["cancelled"] = True

        world.logger.log(
            f"NPC {npc.id} quiso comer pero no tenía comida."
        )

        return

    action.data["food"] = best_food

    world.logger.log(
        f"NPC {npc.id} comenzó a comer {best_food}."
    )
    
    npc.current_location = \
        npc.city.locations[
            LocationType.RESIDENTIAL
        ]


# -------------------------------------------------------
# Tick
# -------------------------------------------------------

def update(action, npc, world):

    if action.data.get("cancelled"):
        return

    # Mientras come recupera un poco de tranquilidad.
    npc.stress = max(
        0,
        npc.stress - 0.2
    )


# -------------------------------------------------------
# Final
# -------------------------------------------------------

def finish(action, npc, world):
    

    if action.data.get("cancelled"):

        npc.hunger += 5
        npc.stress += 0.5
        return

    food = action.data["food"]

    definition = RESOURCES[food]

    npc.inventory[food] -= 1

    npc.hunger = max(
        0,
        npc.hunger - definition.nutrition
    )

    npc.satiety += definition.nutrition * 0.5

    npc.energy += 5

    npc.happiness += definition.happiness_bonus

    npc.memory.record_short(
        f"ate_{food}"
    )

    world.logger.log(
        f"NPC {npc.id} terminó de comer {food}."
    )