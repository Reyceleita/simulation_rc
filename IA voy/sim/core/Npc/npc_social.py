"""
npc_social.py
Handles relationship tracking and social interactions between NPCs.
"""

import random


class NPCSocial:
    """
    Manages an NPC's relationships and the logic for choosing
    and executing social interactions.
    """

    def __init__(self):
        # {npc_id: float}  values in [-1, 1]
        self.relationships: dict[int, float] = {}

    # ------------------------------------------------------------------
    # Relationship helpers
    # ------------------------------------------------------------------

    def average_relationship(self) -> float:
        if not self.relationships:
            return 0.0
        return sum(self.relationships.values()) / len(self.relationships)

    def get_relation(self, npc_id: int) -> float:
        return self.relationships.get(npc_id, 0.0)

    def _apply_change(self, npc_id: int, change: float):
        self.relationships.setdefault(npc_id, 0.0)
        self.relationships[npc_id] = max(
            -1.0, min(1.0, self.relationships[npc_id] + change)
        )

    # ------------------------------------------------------------------
    # Target selection
    # ------------------------------------------------------------------

    def choose_social_target(self, self_id: int, world):
        """
        Pick a candidate NPC to socialize with, weighted by existing
        relationship and impulsiveness.
        """
        candidates = [
            npc for npc in world.npcs
            if npc.id != self_id and npc.id not in world.busy_npcs
        ]
        if not candidates:
            return None

        impulsiveness = 0.0  # caller should pass personality["impulsiveness"]
        weighted = []
        for npc in candidates:
            relation = self.relationships.get(npc.id, 0.0)
            weight = 1.0 + relation
            weighted.append((npc, max(0.1, weight)))

        return _weighted_choice(weighted)

    def choose_social_target_with_personality(
        self, self_id: int, world, impulsiveness: float
    ):
        candidates = [
            npc for npc in world.npcs
            if npc.id != self_id and npc.id not in world.busy_npcs
        ]
        if not candidates:
            return None

        weighted = []
        for npc in candidates:
            relation = self.relationships.get(npc.id, 0.0)
            weight = 1.0 + relation
            if impulsiveness > 0.7:
                weight += abs(relation) * 0.5
            weighted.append((npc, max(0.1, weight)))

        return _weighted_choice(weighted)

    # ------------------------------------------------------------------
    # Interaction resolution
    # ------------------------------------------------------------------

    def interact(self, self_npc, other_npc, world) -> tuple[float, str]:
        """
        Resolve a social interaction between two NPCs.

        Returns (relationship_change, interaction_type).
        Side-effects: updates both NPCs' relationships, happiness, stress.
        """
        compatibility = (
            (self_npc.personality["sociability"] + other_npc.personality["sociability"]) / 2
            + (self_npc.personality["empathy"] + other_npc.personality["empathy"]) / 2
        )
        outcome = compatibility + random.uniform(-0.5, 0.5)

        if outcome > 0.7:
            change = 0.1
            tipo = "amigable"
            self_npc.happiness += 2
        elif outcome < 0.3:
            change = -0.1
            tipo = "conflicto"
            self_npc.stress += 1
        else:
            change = 0.02
            tipo = "neutral"

        # Update both sides
        self_npc.social._apply_change(other_npc.id, change)
        other_npc.social._apply_change(self_npc.id, change)

        world.logger.log(
            f"   🤝 NPC {self_npc.id} → NPC {other_npc.id} | {tipo} "
            f"({change:+.2f}) | relación: {self_npc.social.relationships[other_npc.id]:.2f}"
        )

        return change, tipo


# ------------------------------------------------------------------
# Module-level utility (used internally)
# ------------------------------------------------------------------

def _weighted_choice(actions: list[tuple]) :
    total = sum(w for _, w in actions)
    r = random.uniform(0, total)
    upto = 0.0
    for item, weight in actions:
        if upto + weight >= r:
            return item
        upto += weight
    return actions[-1][0]