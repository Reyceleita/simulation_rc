"""
buy.py

Handler de la acción BUY.

Responsabilidad:
Comprar UN recurso específico.

"""

from sim.core.City.location_registry import LocationType
from sim.core.Npc_AI.planner.helpers.shopping import calculate_cost


# -------------------------------------------------------------
# Inicio
# -------------------------------------------------------------

def start(action, npc, world):
    
    print("Comenzó a comprar")

    resource = action.data["resource"]
    amount = action.data["amount"]

    world.logger.log(
        f"NPC {npc.id} comenzó a comprar "
        f"{amount} x {resource}"
    )
    
    npc.current_location = \
        npc.city.locations[
            LocationType.SHOPPING
        ]


# -------------------------------------------------------------
# Tick
# -------------------------------------------------------------

def update(action, npc, world):

    # La compra es instantánea.
    pass


# -------------------------------------------------------------
# Final
# -------------------------------------------------------------

def finish(action, npc, world):
    
    print("Compró")

    resource = action.data["resource"]
    amount = action.data["amount"]

    city = npc.city

    # ------------------------------------
    # Precio
    # ------------------------------------

    cost = calculate_cost(
        city,
        resource,
        amount
    )

    if cost is None:
        return

    # ------------------------------------
    # Dinero
    # ------------------------------------

    if npc.money < cost:

        world.logger.log(

            f"NPC {npc.id} no pudo comprar "
            f"{resource}: dinero insuficiente."

        )

        return

    # ------------------------------------
    # Stock
    # ------------------------------------

    if not city.consume_resource(
        resource,
        amount
    ):

        world.logger.log(

            f"NPC {npc.id} no pudo comprar "
            f"{resource}: sin stock."

        )

        return

    # ------------------------------------
    # Compra
    # ------------------------------------

    npc.money -= cost

    npc.inventory[resource] = (

        npc.inventory.get(resource, 0)

        + amount

    )

    npc.memory.record_short(

        f"buy_{resource}"

    )

    world.logger.log(

        f"NPC {npc.id} compró "
        f"{amount} x {resource} "
        f"(${cost:.2f})"

    )