"""
    Acción de trabajar
"""


import random

from sim.core.City.location_registry import LocationType


AGRICULTURAL_PRODUCES = ["wheat", "meat", "vegetables"]


def start(action, npc, world):
    npc.memory.record_short("started_work")
    npc.current_location = \
        npc.city.locations[
            LocationType.WORK
        ]


def update(action, npc, world):
    npc.energy -= 4
    npc.hunger += 2
    npc.stress += npc.job["stress_gain"]


def finish(action, npc, world):
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

        npc.city.add_resource(
            resource,
            produced
        )
    npc.memory.record_short("worked")