"""
stats_tracker.py
Responsabilidad: Recolección, almacenamiento y cálculo de estadísticas.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class NPCStatsSnapshot:
    """Snapshot de estadísticas de un NPC en un momento dado."""
    money: float
    hunger: float
    happiness: float
    stress: float


@dataclass  
class GlobalStatsSnapshot:
    """Snapshot de estadísticas globales del mundo."""
    money: float
    hunger: float
    happiness: float
    stress: float


class StatsTracker:
    """
    Responsable de:
    - Almacenar historial de estadísticas por NPC
    - Calcular promedios globales
    - Proveer datos para visualización
    """

    def __init__(self):
        self.global_history: Dict[str, List[float]] = {
            "money": [],
            "hunger": [],
            "happiness": [],
            "stress": []
        }
        self.npc_history: Dict[int, Dict[str, List[float]]] = {}

    def register_npc(self, npc_id: int) -> None:
        """Registra un nuevo NPC para tracking."""
        self.npc_history[npc_id] = {
            "money": [],
            "hunger": [],
            "happiness": [],
            "stress": []
        }

    def record_npc_stats(self, npc_id: int, snapshot: NPCStatsSnapshot) -> None:
        """Registra estadísticas de un NPC."""
        if npc_id not in self.npc_history:
            self.register_npc(npc_id)

        self.npc_history[npc_id]["money"].append(snapshot.money)
        self.npc_history[npc_id]["hunger"].append(snapshot.hunger)
        self.npc_history[npc_id]["happiness"].append(snapshot.happiness)
        self.npc_history[npc_id]["stress"].append(snapshot.stress)

    def record_global_stats(self, snapshot: GlobalStatsSnapshot) -> None:
        """Registra estadísticas globales."""
        self.global_history["money"].append(snapshot.money)
        self.global_history["hunger"].append(snapshot.hunger)
        self.global_history["happiness"].append(snapshot.happiness)
        self.global_history["stress"].append(snapshot.stress)

    def calculate_global_averages(self, npcs: List[Any]) -> GlobalStatsSnapshot:
        """Calcula promedios globales a partir de una lista de NPCs."""
        if not npcs:
            return GlobalStatsSnapshot(0, 0, 0, 0)

        total = len(npcs)
        return GlobalStatsSnapshot(
            money=sum(n.money for n in npcs) / total,
            hunger=sum(n.hunger for n in npcs) / total,
            happiness=sum(n.happiness for n in npcs) / total,
            stress=sum(n.stress for n in npcs) / total
        )

    def get_npc_history(self, npc_id: int) -> Dict[str, List[float]]:
        """Obtiene historial de un NPC específico."""
        return self.npc_history.get(npc_id, {})

    def get_global_history(self) -> Dict[str, List[float]]:
        """Obtiene historial global."""
        return self.global_history
