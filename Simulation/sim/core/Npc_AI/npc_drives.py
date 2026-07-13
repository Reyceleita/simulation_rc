"""
npc_drives.py
Computes action drives and selects the NPC's next action each tick.
All drive weights live here so tuning is centralised.
"""

import random

from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import ResourceCategory
from sim.utils.helpers.resources_helpers import get_category_stock, get_inventory_value


# ------------------------------------------------------------------
# Time-block helper
# ------------------------------------------------------------------

def get_time_block(hour: int) -> str:
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 22:
        return "evening"
    return "night"


# ------------------------------------------------------------------
# Drive calculator
# ------------------------------------------------------------------

def calculate_drives(npc, world) -> dict[str, float]:
    """
    Compute a score for every possible action the NPC could take.
    Higher score = stronger motivation.

    Parameters
    ----------
    npc   : NPC  — the full NPC object (stats + memory + social attached)
    world : World
    """
    drives: dict[str, float] = {}
    culture = npc.city.culture
    hour = world.time_manager.hour

    # ----------------------------------------------------------------
    # 🍔  EAT
    # ----------------------------------------------------------------
    if npc.satiety < 30:
        if npc.hunger > npc.hunger_threshold:
            drives["eat"] = ((npc.hunger - npc.hunger_threshold) / 100) * 8
        else:
            drives["eat"] = 0.2
    else:
        drives["eat"] = 0.0

    # ----------------------------------------------------------------
    # 🛒  BUY FOOD
    # ----------------------------------------------------------------
    
    food_stock = get_category_stock(
        npc,
        ResourceCategory.FOOD
    )
    
    food_drive = max(
    0,
    3 - food_stock
)

    food_drive += npc.hunger / 50

    food_drive *= (
        1.0
        - npc.personality["greed"] * 0.2
    )

    if npc.money < 20:
        food_drive *= 0.7

    drives["buy_food"] = food_drive

    # ----------------------------------------------------------------
    # 🛍️  BUY RESOURCES
    # ----------------------------------------------------------------

    need = max(
        0,
        (70 - npc.happiness) / 20
    )
    
    wealth_factor = min(
        2.0,
        0.5 + npc.money / 200
    )
    
    
    drives["buy_consumer_goods"] = (
        need *
        wealth_factor 
    )
    
    drives["buy_consumer_goods"] = min(
        3,
        need * wealth_factor
    )
    
    # ----------------------------------------------------------------
    # 🛍️  BUY LUXURY
    # ----------------------------------------------------------------
    
    if npc.money > 50:

        luxury_drive = (
            npc.personality["impulsiveness"]
            + npc.personality["greed"] * -0.5
        )

        luxury_drive += (
            100 - npc.happiness
        ) / 50
        
        drives["buy_luxury"] = max(
            0,
            luxury_drive
        )

    # ----------------------------------------------------------------
    # 💼  WORK
    # ----------------------------------------------------------------
    if npc.profession == "unemployed":
        drives["work"] = 0.0
    elif hour in npc.job.get("work_hours", []):
        drives["work"] = (
            1.0
            + npc.personality["discipline"] * 0.7
            + (1 - npc.money / 200)
            + (npc.hunger / 100) * 4
        )
        drives["work"] += culture["discipline"] * 0.3
        if npc.money < 30:
            drives["work"] += 2
    else:
        drives["work"] = 0.0
        
    wealth = (
        npc.money
        + get_inventory_value(npc)
    )
    
    if wealth < 50:
        drives["work"] += 1
    
    if wealth < 20:
        drives["work"] += 2
    
    if wealth < 5:
        drives["work"] += 2

    # ----------------------------------------------------------------
    # 🧑‍🤝‍🧑  SOCIALIZE
    # ----------------------------------------------------------------
    if 18 <= hour <= 22:
        drives["socialize"] = (
            npc.personality["sociability"] * 0.8
            + npc.memory.memory_emotional["social_satisfaction"]
        )
    else:
        drives["socialize"] = 0.2 * npc.personality["sociability"]

    avg_relation = npc.social.average_relationship()
    drives["socialize"] += avg_relation * 0.5
    drives["socialize"] += culture["sociability"] * 0.3
    
    drives["socialize"] += max(
        0,
        avg_relation
    ) * 0.5

    # ----------------------------------------------------------------
    # 😴  REST
    # ----------------------------------------------------------------
    if hour >= 22 or hour <= 5:
        drives["rest"] = 1.5 + (100 - npc.energy) / 100
    else:
        drives["rest"] = (100 - npc.energy) / 50

    # ----------------------------------------------------------------
    # 🚚  TRADER-SPECIFIC
    # ----------------------------------------------------------------
    if npc.profession == "trader":
        _add_trader_drives(drives, npc, world)

    return drives


def _add_trader_drives(drives: dict, npc, world):

    best_route = None
    best_profit = 0.0

    for route in world.trade_manager.routes:

        if route.profit > best_profit:
            best_profit = route.profit
            best_route = route

    if not best_route:
        drives.setdefault("trade_buy", 0.0)
        drives.setdefault("travel", 0.0)
        drives.setdefault("trade_sell", 0.0)
        return

    npc.trade_route = best_route

    resource = best_route.resource

    cargo_amount = npc.cargo.get(resource, 0)

    greed_bonus = 1 + npc.personality["greed"]
    risk_bonus = 1 + npc.personality["risk"] * 0.5

    # Comprar recurso en ciudad origen
    if npc.city == best_route.origin and cargo_amount == 0:

        drives["trade_buy"] = (
            best_profit
            * 1.5
            * greed_bonus
        )

    # Viajar hacia destino
    elif cargo_amount > 0 and npc.city != best_route.destination:

        drives["travel"] = (
            best_profit
            * 2
            * risk_bonus
        )

    # Vender recurso en destino
    elif npc.city == best_route.destination and cargo_amount > 0:

        drives["trade_sell"] = (
            best_profit
            * 2
            * greed_bonus
        )


# ------------------------------------------------------------------
# Decision selector
# ------------------------------------------------------------------

def select_action(npc, world) -> str:
    """
    Calculate drives, apply routine + personality noise, return the
    winning action name.
    """
    drives = calculate_drives(npc, world)

    time_block = get_time_block(world.time_manager.hour)
    planned = npc.schedule.get(time_block, "rest")

    # Routine reinforcement (discipline) — only when not starving
    if npc.hunger < 70:
        drives[planned] = drives.get(planned, 0.0) + 0.5 * npc.personality["discipline"]

    # Impulsive noise
    for k in list(drives):
        noise = random.uniform(-0.2, 0.2) * npc.personality["impulsiveness"]
        drives[k] += noise

    return max(drives, key=drives.get)