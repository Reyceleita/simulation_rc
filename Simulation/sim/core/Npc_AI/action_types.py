"""
Tipos de acciones que puede realizar un NPC.
"""

from enum import Enum, auto


class ActionType(Enum):

    # -------------------------
    # Necesidades básicas
    # -------------------------

    EAT = auto()
    SLEEP = auto()
    REST = auto()

    # -------------------------
    # Economía
    # -------------------------

    WORK = auto()

    # -------------------------
    # Comercio
    # -------------------------

    BUY = auto()
    SELL = auto()

    # -------------------------
    # Movimiento
    # -------------------------

    TRAVEL = auto()

    # -------------------------
    # Social
    # -------------------------

    SOCIALIZE = auto()

    # -------------------------
    # Producción
    # -------------------------

    FARM = auto()
    CRAFT = auto()