"""
npc_drives.py
Computes action drives and selects the NPC's next action each tick.
All drive weights live here so tuning is centralised.
"""

import random


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
    desired_food = 5
    drives["buy_food"] = max(0.0, desired_food - npc.inventory["food"]) * 0.8

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
        drives.setdefault("trade_sell", 0.0)
        return

    npc.trade_route = best_route

    if npc.city == best_route.origin and npc.cargo["food"] == 0:
        drives["trade_buy"] = best_profit * 1.5
    elif npc.cargo["food"] > 0 and npc.city != best_route.destination:
        drives["travel"] = best_profit * 2
    elif npc.city == best_route.destination and npc.cargo["food"] > 0:
        drives["trade_sell"] = best_profit * 2


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