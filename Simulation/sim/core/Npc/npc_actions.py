"""
npc_actions.py
Executes a chosen action, mutating NPC and world state accordingly.
Each action is an isolated function for easy testing and extension.
"""

import random

from sim.snapshots.decision_snapshot import DecisionSnapshot

# ------------------------------------------------------------------
# Public dispatcher
# ------------------------------------------------------------------

def execute_action(npc, action: str, world):
    """Route `action` to the correct handler."""

    # Emergency eat — bypasses normal action selection
    if npc.hunger > 85 and npc.city.resources["food"] > 0:
        _emergency_eat(npc)
        return

    handlers = {
        "eat": _eat,
        "work": _work,
        "socialize": _socialize,
        "rest": _rest,
        "buy_food": _buy_food,
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
    npc.city.resources["food"] -= 1
    npc.hunger -= 25


def _eat(npc, world):
    if npc.inventory["food"] > 0:
        npc.inventory["food"] -= 1
        food_value = random.randint(20, 35)
        npc.hunger -= food_value
        npc.satiety += 20
        npc.happiness += 2
        npc.energy += 5
        npc.stress -= 1
        npc.memory.record_short("ate")
    else:
        npc.hunger += 5
        npc.stress += 0.5


def _work(npc, world):
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

    income = int(base_income * npc.city.economy.economic_factor * efficiency)
    npc.money += income

    produces = npc.job.get("produces")
    base_output = npc.job.get("base_output", 0)

    if produces:
        bonus = npc.city.production.production_bonus.get(produces, 1.0)
        raw = base_output * efficiency * bonus * random.uniform(0.9, 1.1)
        produced = int(raw) + (1 if random.random() < (raw % 1) else 0)
        npc.city.resources[produces] += produced

    npc.stress += npc.job["stress_gain"]
    npc.memory.record_short("worked")


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
    amount = min(3, npc.city.resources["food"])
    price = npc.city.cost_of_life["food_price"]
    cost = amount * price

    if npc.money >= cost:
        npc.money -= cost
        npc.city.economy.treasury += cost
        npc.city.resources["food"] -= amount
        npc.inventory["food"] += amount


def _travel(npc, world):
    if not npc.trade_route or npc.profession != "trader":
        return

    npc.travel_timer += 1

    if npc.travel_timer >= 3:
        if npc in npc.city.npcs:
            npc.city.npcs.remove(npc)

        npc.city = (
            npc.trade_route.destination
            if npc.cargo["food"] > 0
            else npc.trade_route.origin
        )
        npc.city.npcs.append(npc)
        npc.travel_timer = 0


def _trade_buy(npc, world):
    city_food = npc.city.resources["food"]
    if city_food <= 0:
        return

    price = npc.city.cost_of_life["food_price"]
    amount = min(50, city_food, int(npc.money / price))

    if amount <= 0:
        return

    npc.money -= amount * price
    npc.city.resources["food"] -= amount
    npc.cargo["food"] += amount


def _trade_sell(npc, world):
    npc.city.resources["food"] += npc.cargo["food"]
    npc.cargo["food"] = 0

