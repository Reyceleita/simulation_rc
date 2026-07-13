"""
Objetivos de inventario.
"""

from sim.core.resources.resources_types import ResourceCategory


def get_targets(npc):

    targets = {}

    # -----------------------
    # Comida
    # -----------------------

    discipline = npc.personality["discipline"]

    impulsiveness = npc.personality["impulsiveness"]

    days = int(

        7

        + discipline * 3

        - impulsiveness * 2

    )

    days = max(3, days)

    targets[ResourceCategory.FOOD] = days * 2

    # -----------------------
    # Bienes de consumo
    # -----------------------

    targets[ResourceCategory.CONSUMER] = 3

    # -----------------------
    # Lujo
    # -----------------------

    targets[ResourceCategory.LUXURY] = 1

    return targets