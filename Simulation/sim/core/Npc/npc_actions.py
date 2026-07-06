"""
npc_actions.py
Executes a chosen action, mutating NPC and world state accordingly.
Each action is an isolated function for easy testing and extension.
"""

import random

from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import ResourceCategory
from sim.snapshots.decision_snapshot import DecisionSnapshot

# ------------------------------------------------------------------
# Public dispatcher
# ------------------------------------------------------------------

AGRICULTURAL_PRODUCES = ["wheat", "meat", "vegetables"]

def execute_action(npc, action: str, world):
    """
    Ejecuta una acción.

    Si el NPC está en estado crítico de hambre y existe comida
    en la ciudad, intenta comer inmediatamente.
    """

    city_food = npc.city.get_resources_by_category(
        ResourceCategory.FOOD
    )

    food_available = any(
        amount > 0
        for amount in city_food.values()
    )

    if npc.hunger > 85 and food_available:
        _emergency_eat(npc)
        return

    handlers = {
        "eat": _eat,
        "work": _work,
        "socialize": _socialize,
        "rest": _rest,
        "buy_food": _buy_food,
        "buy_consumer_goods": _buy_consumer_goods,
        "buy_luxury": _buy_luxury,
        "travel": _travel,
        "trade_buy": _trade_buy,
        "trade_sell": _trade_sell,
    }

    handler = handlers.get(action)

    if handler:
        handler(npc, world)


# ------------------------------------------------------------------
# Individual action handlers
# ------------------------------------------------------------------

def _emergency_eat(npc):

    best_food = None
    best_nutrition = 0

    for resource_name, amount in npc.inventory.items():

        if amount <= 0:
            continue

        definition = RESOURCES.get(resource_name)

        if (
            definition
            and definition.category == ResourceCategory.FOOD
            and definition.nutrition > best_nutrition
        ):
            best_food = resource_name
            best_nutrition = definition.nutrition

    if best_food:

        npc.inventory[best_food] -= 1

        npc.hunger -= best_nutrition
        npc.satiety += best_nutrition * 0.5


def _eat(npc, world):

    best_food = None
    best_nutrition = 0

    for resource_name, amount in npc.inventory.items():

        if amount <= 0:
            continue

        definition = RESOURCES.get(resource_name)

        if (
            definition
            and definition.category == ResourceCategory.FOOD
            and definition.nutrition > best_nutrition
        ):
            best_food = resource_name
            best_nutrition = definition.nutrition

    if not best_food:
        npc.hunger += 5
        npc.stress += 0.5
        return

    definition = RESOURCES[best_food]

    npc.inventory[best_food] -= 1

    npc.hunger -= definition.nutrition
    npc.satiety += definition.nutrition * 0.5

    npc.happiness += definition.happiness_bonus
    npc.energy += 5

    npc.memory.record_short(f"ate_{best_food}")


def _work(npc, world):
    """
    Trabajar genera dinero y produce recursos para la ciudad.
    """

    base_income = npc.job["base_salary"]

    efficiency = (
        1
        + npc.personality["discipline"] * 0.5
        - npc.stress / 200
    )

    physical_factor = (
        0.85
        + (npc.energy / 100) * 0.1
        + (1 - npc.hunger / 100) * 0.05
    )

    efficiency *= physical_factor

    income = int(
        base_income
        * npc.city.economy.economic_factor
        * efficiency
    )

    npc.money += income

    produces = npc.job.get("produces")
    
    base_output = npc.job.get("base_output", 0)

    if produces == "agriculture":
        resource = random.choice(AGRICULTURAL_PRODUCES)

        bonus = npc.city.production.production_bonus.get(
            resource,
            1.0
        )

        raw = (
            base_output
            * efficiency
            * bonus
            * random.uniform(0.9, 1.1)
        )

        produced = int(raw)

        if random.random() < (raw % 1):
            produced += 1

        # CORREGIDO:
        npc.city.add_resource(
            resource,
            produced
        )

    npc.stress += npc.job["stress_gain"]

    npc.memory.record_short("worked")

def _buy_consumer_goods(npc, world):

    consumer_market = npc.city.get_resources_by_category(
        ResourceCategory.CONSUMER
    )

    if not consumer_market:
        return

    cheapest_resource = None
    cheapest_price = float("inf")

    for resource_name, amount in consumer_market.items():

        if amount <= 0:
            continue

        definition = RESOURCES.get(resource_name)

        if not definition:
            continue

        if definition.base_price < cheapest_price:
            cheapest_price = definition.base_price
            cheapest_resource = resource_name

    if not cheapest_resource:
        return

    if npc.money < cheapest_price:
        return

    npc.money -= cheapest_price

    npc.city.consume_resource(
        cheapest_resource,
        1
    )

    npc.inventory[cheapest_resource] = (
        npc.inventory.get(cheapest_resource, 0)
        + 1
    )

    npc.happiness += 3

    npc.memory.record_short(
        f"bought_{cheapest_resource}"
    )

def _buy_luxury(npc, world):

    luxury_market = npc.city.get_resources_by_category(
        ResourceCategory.LUXURY
    )

    if not luxury_market:
        return

    cheapest_resource = None
    cheapest_price = float("inf")

    for resource_name, amount in luxury_market.items():

        if amount <= 0:
            continue

        definition = RESOURCES.get(resource_name)

        if not definition:
            continue

        if definition.base_price < cheapest_price:
            cheapest_price = definition.base_price
            cheapest_resource = resource_name

    if not cheapest_resource:
        return

    if npc.money < cheapest_price:
        return

    npc.money -= cheapest_price

    npc.city.consume_resource(
        cheapest_resource,
        1
    )

    npc.inventory[cheapest_resource] = (
        npc.inventory.get(cheapest_resource, 0)
        + 1
    )

    npc.happiness += 8

    npc.memory.record_short(
        f"luxury_{cheapest_resource}"
    )

def _socialize(npc, world):
    target = npc.social.choose_social_target_with_personality(
        npc.id, world, npc.personality["impulsiveness"]
    )

    if not target:
        return

    world.busy_npcs.add(npc.id)
    world.busy_npcs.add(target.id)

    change, _ = npc.social.interact(npc, target, world)

    world.logger.log(
        f"NPC {npc.id} interactúa con NPC {target.id} ({change:+.2f})"
    )

    npc.memory.record_short("socialized")
    npc.energy -= 5
    npc.happiness += 4
    npc.stress -= 3


def _rest(npc, world):
    npc.energy += 15
    npc.stress -= 0.2
    npc.hunger += 2
    npc.memory.record_short("rested")


def _buy_food(npc, world):
    """
    Compra comida de la ciudad.

    Busca el alimento más barato disponible.
    """

    food_market = npc.city.get_resources_by_category(
        ResourceCategory.FOOD
    )

    cheapest = None
    cheapest_price = float("inf")

    for resource_name, stock in food_market.items():

        if stock <= 0:
            continue

        price = npc.city.prices.get(resource_name)

        if price is None:
            continue

        if price < cheapest_price:
            cheapest = resource_name
            cheapest_price = price

    if not cheapest:
        return

    amount = 3

    cost = amount * cheapest_price

    if npc.money < cost:
        return

    success = npc.city.consume_resource(
        cheapest,
        amount
    )

    if not success:
        return

    npc.money -= cost

    npc.inventory[cheapest] = (
        npc.inventory.get(cheapest, 0)
        + amount
    )

    npc.memory.record_short(
        f"bought_{cheapest}"
    )


def _travel(npc, world):
    """
    Movimiento del comerciante entre ciudades.
    """

    if not npc.trade_route:
        return

    if npc.profession != "trader":
        return

    npc.travel_timer += 1

    if npc.travel_timer < 3:
        return

    if npc in npc.city.npcs:
        npc.city.npcs.remove(npc)

    has_cargo = any(
        amount > 0
        for amount in npc.cargo.values()
    )

    npc.city = (
        npc.trade_route.destination
        if has_cargo
        else npc.trade_route.origin
    )

    npc.city.npcs.append(npc)

    npc.travel_timer = 0


def _trade_buy(npc, world):
    """
    Compra mercancía en la ciudad de origen.
    """

    route = npc.trade_route

    if not route:
        return

    resource = route.resource

    stock = npc.city.resources.get(
        resource,
        0
    )

    if stock <= 0:
        return

    price = npc.city.prices.get(resource)

    if price is None:
        return

    amount = min(
        route.amount,
        stock,
        int(npc.money / price)
    )

    if amount <= 0:
        return

    success = npc.city.consume_resource(
        resource,
        amount
    )

    if not success:
        return

    npc.money -= amount * price

    npc.cargo[resource] = (
        npc.cargo.get(resource, 0)
        + amount
    )

    npc.memory.record_short(
        f"trade_buy_{resource}"
    )

def _trade_sell(npc, world):
    """
    Vende mercancía en la ciudad destino.
    """

    route = npc.trade_route

    if not route:
        return

    resource = route.resource

    amount = npc.cargo.get(
        resource,
        0
    )

    if amount <= 0:
        return

    price = npc.city.prices.get(resource)

    if price is None:
        return

    revenue = amount * price

    npc.money += revenue

    npc.city.add_resource(
        resource,
        amount
    )

    npc.cargo[resource] = 0

    npc.memory.record_short(
        f"trade_sell_{resource}"
    )
