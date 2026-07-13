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

    def choose_target(self, npc, world):

        candidates = []
    
        for other in world.npcs:
        
            if other.id == npc.id:
                continue
            
            if other.current_action is not None:
                continue
            
            relation = self.relationships.get(
                other.id,
                0.0
            )
    
            weight = 1 + relation
    
            if npc.personality["impulsiveness"] > 0.7:
            
                weight += abs(relation) * 0.5
    
            candidates.append(
                (
                    other,
                    max(weight, 0.1)
                )
            )
    
        if not candidates:
            return None
    
        return _weighted_choice(candidates)
    # ------------------------------------------------------------------
    # Interaction resolution
    # ------------------------------------------------------------------

    def resolve_interaction(
        self,
        npc,
        target,
        world
    ) -> dict:
        """
        Resuelve una interacción social entre dos NPC.

        Se encarga de:
            - calcular el resultado
            - modificar relaciones
            - modificar estados emocionales
            - registrar memoria

        Devuelve información útil para el logger.
        """

        compatibility = (

            (
                npc.personality["sociability"]
                + target.personality["sociability"]
            ) / 2

            +

            (
                npc.personality["empathy"]
                + target.personality["empathy"]
            ) / 2

        )

        outcome = compatibility + random.uniform(-0.5, 0.5)

        if outcome > 0.7:

            relationship_change = 0.10

            happiness = 2

            stress = 0

            interaction_type = "friendly"

        elif outcome < 0.3:

            relationship_change = -0.10

            happiness = 0

            stress = 1

            interaction_type = "conflict"

        else:

            relationship_change = 0.02

            happiness = 1

            stress = 0

            interaction_type = "neutral"

        # -------------------------
        # Relaciones
        # -------------------------

        self._apply_change(
            target.id,
            relationship_change
        )

        target.social._apply_change(
            npc.id,
            relationship_change
        )

        # -------------------------
        # Estados
        # -------------------------

        npc.happiness += happiness
        target.happiness += happiness

        npc.stress += stress
        target.stress += stress

        # -------------------------
        # Memorias
        # -------------------------

        npc.memory.record_short("socialized")
        target.memory.record_short("socialized")

        return {

            "type": interaction_type,

            "relationship_change": relationship_change

        }


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