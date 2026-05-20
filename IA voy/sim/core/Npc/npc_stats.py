import random


def default_personality() -> dict:
    return {
        "greed": random.random(),
        "sociability": random.random(),
        "risk": random.random(),
        "discipline": random.random(),
        "empathy": random.random(),
        "impulsiveness": random.random(),
    }


def default_schedule() -> dict:
    return {
        "morning": "work",
        "afternoon": "work",
        "evening": "socialize",
        "night": "rest",
    }


def default_inventory() -> dict:
    return {
        "food": random.randint(1, 3),
        "goods": 0,
    }


def default_cargo() -> dict:
    return {"food": 0}


class NPCStats:
    """
    Holds and initializes all raw numerical state for an NPC.
    No logic here — only data and clamping helpers.
    """

    def __init__(self):
        self.money: float = random.randint(20, 100)
        self.hunger: float = random.randint(0, 30)
        self.energy: float = 100.0
        self.happiness: float = 50.0
        self.stress: float = 25.0
        self.satiety: float = 0.0

        self.metabolism: float = random.uniform(0.7, 1.4)
        self.hunger_threshold: int = random.randint(35, 75)

        self.personality: dict = default_personality()
        self.schedule: dict = default_schedule()
        self.inventory: dict = default_inventory()
        self.cargo: dict = default_cargo()

        # Location / travel
        self.city = None
        self.travel_target = None
        self.travel_timer: int = 0
        self.trade_route = None

        # Profession / job (set externally)
        self.profession: str = "unemployed"
        self.job: dict = {}

    def clamp_all(self):
        """Clamp every bounded stat to its valid range."""
        self.hunger = max(0.0, min(100.0, self.hunger))
        self.happiness = max(0.0, min(100.0, self.happiness))
        self.energy = max(0.0, min(100.0, self.energy))
        self.stress = max(0.0, min(100.0, self.stress))
        self.satiety = max(0.0, min(100.0, self.satiety))