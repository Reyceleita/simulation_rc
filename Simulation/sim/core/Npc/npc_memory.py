"""
npc_memory.py
Manages short-term event counters and long-term emotional satisfaction scores.
"""


class NPCMemory:
    """
    Encapsulates the NPC's two memory layers:
        - memory_short  : recent activity counters (decay fast)
        - memory_emotional : satisfaction scores in [0, 1] (decay slowly)
    """

    DECAY_SHORT: float = 0.8
    DECAY_EMOTIONAL: float = 0.995

    def __init__(self):
        self.memory_short: dict[str, float] = {
            "worked": 0.0,
            "socialized": 0.0,
            "rested": 0.0,
            "ate": 0.0,
        }
        self.memory_emotional: dict[str, float] = {
            "job_satisfaction": 0.5,
            "social_satisfaction": 0.5,
            "life_satisfaction": 0.5,
        }

    # ------------------------------------------------------------------
    # Decay
    # ------------------------------------------------------------------

    def decay(self):
        """Apply per-tick decay to both memory layers."""
        for key in self.memory_short:
            self.memory_short[key] *= self.DECAY_SHORT
        for key in self.memory_emotional:
            self.memory_emotional[key] *= self.DECAY_EMOTIONAL

    # ------------------------------------------------------------------
    # Updates driven by actions
    # ------------------------------------------------------------------

    def record_action(self, action: str, personality: dict, hunger: float):
        """Update emotional memory based on what the NPC just did."""
        if action == "work":
            self.memory_emotional["job_satisfaction"] += (
                0.05 * personality["discipline"]
            )
        elif action == "socialize":
            self.memory_emotional["social_satisfaction"] += (
                0.02 * personality["sociability"]
            )

        if hunger >= 80:
            self.memory_emotional["life_satisfaction"] -= 0.05

        self._clamp()

    def record_short(self, key: str, amount: float = 1.0):
        """Increment a short-term activity counter."""
        if key in self.memory_short:
            self.memory_short[key] += amount

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clamp(self):
        for k in self.memory_emotional:
            self.memory_emotional[k] = max(0.0, min(1.0, self.memory_emotional[k]))