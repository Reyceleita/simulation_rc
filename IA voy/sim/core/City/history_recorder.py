"""
history_recorder.py
Responsabilidad: Registro y almacenamiento de métricas históricas.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class CitySnapshot:
    """Snapshot de métricas de una ciudad en un momento dado."""
    food: float
    population: int
    employed: int
    unemployed: int
    food_price: int
    avg_hunger: float
    avg_money: float
    avg_stress: float
    avg_happiness: float


class HistoryRecorder:
    """
    Responsable de:
    - Almacenar series temporales de métricas de la ciudad
    - Proveer datos para análisis y visualización
    """

    def __init__(self):
        self.history: Dict[str, List] = {
            "food": [],
            "goods": [],
            "prices": [],
            "population": [],
            "employed": [],
            "unemployed": [],
            "hunger": [],
            "money": [],
            "stress": [],
            "happiness": []
        }

    def record(self, snapshot: CitySnapshot) -> None:
        """Registra un snapshot de métricas."""
        self.history["food"].append(snapshot.food)
        self.history["population"].append(snapshot.population)
        self.history["employed"].append(snapshot.employed)
        self.history["unemployed"].append(snapshot.unemployed)
        self.history["prices"].append(snapshot.food_price)
        self.history["hunger"].append(snapshot.avg_hunger)
        self.history["money"].append(snapshot.avg_money)
        self.history["stress"].append(snapshot.avg_stress)
        self.history["happiness"].append(snapshot.avg_happiness)

    def get_history(self, metric: str) -> List:
        """Retorna historial de una métrica específica."""
        return self.history.get(metric, [])

    def get_all_history(self) -> Dict[str, List]:
        """Retorna todo el historial."""
        return self.history.copy()

    def get_latest(self, metric: str) -> Any:
        """Retorna último valor registrado de una métrica."""
        data = self.history.get(metric, [])
        return data[-1] if data else None

    def clear(self) -> None:
        """Limpia todo el historial."""
        for key in self.history:
            self.history[key] = []
