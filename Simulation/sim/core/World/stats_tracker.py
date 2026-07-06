"""
stats_tracker.py
Responsabilidad: Recolección, almacenamiento y cálculo de estadísticas.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

from sim.core.resources.resources_types import ResourceCategory
from sim.core.resources.global_resources import RESOURCES


@dataclass
class NPCStatsSnapshot:
    """Snapshot de estadísticas de un NPC en un momento dado."""

    money: float
    hunger: float
    happiness: float
    stress: float


@dataclass
class GlobalStatsSnapshot:

    money: float
    hunger: float
    happiness: float
    stress: float

    population: int

    total_market_value: float

    total_food: float

    total_materials: float

    total_industrial: float

    total_consumer: float

    total_luxury: float

    total_energy: float

    total_illegal: float


@dataclass
class CityStatsSnapshot:

    market_value: float

    population: int

    food: float

    materials: float

    industrial: float

    consumer: float

    luxury: float

    energy: float

    illegal: float


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
            "stress": [],
            "population": [],
            "total_market_value": [],
            "total_food": [],
            "total_materials": [],
            "total_industrial": [],
            "total_consumer": [],
            "total_luxury": [],
            "total_energy": [],
            "total_illegal": [],
        }
        self.npc_history: Dict[int, Dict[str, List[float]]] = {}
        self.resource_history = {}
        self.city_history: Dict[str, Dict[str, List[float]]] = {}

        self.resource_history = {resource_name: [] for resource_name in RESOURCES}

    def register_npc(self, npc_id: int) -> None:
        """Registra un nuevo NPC para tracking."""
        self.npc_history[npc_id] = {
            "money": [],
            "hunger": [],
            "happiness": [],
            "stress": [],
        }

    def register_city(self, city_name: str):
        self.city_history[city_name] = {
            "market_value": [],
            "population": [],
            "food": [],
            "materials": [],
            "industrial": [],
            "consumer": [],
            "luxury": [],
            "energy": [],
            "illegal": [],
        }

    def record_npc_stats(self, npc_id: int, snapshot: NPCStatsSnapshot) -> None:
        """Registra estadísticas de un NPC."""
        if npc_id not in self.npc_history:
            self.register_npc(npc_id)

        self.npc_history[npc_id]["money"].append(snapshot.money)
        self.npc_history[npc_id]["hunger"].append(snapshot.hunger)
        self.npc_history[npc_id]["happiness"].append(snapshot.happiness)
        self.npc_history[npc_id]["stress"].append(snapshot.stress)

    def record_city_stats(self, city_name: str, snapshot: CityStatsSnapshot):
        
        if city_name not in self.city_history:
            self.register_city(city_name)

        self.city_history[city_name]["market_value"].append(snapshot.market_value)

        self.city_history[city_name]["population"].append(snapshot.population)

        self.city_history[city_name]["food"].append(snapshot.food)

        self.city_history[city_name]["materials"].append(snapshot.materials)

        self.city_history[city_name]["industrial"].append(snapshot.industrial)

        self.city_history[city_name]["consumer"].append(snapshot.consumer)

        self.city_history[city_name]["luxury"].append(snapshot.luxury)

        self.city_history[city_name]["energy"].append(snapshot.energy)

        self.city_history[city_name]["illegal"].append(snapshot.illegal)

    def record_global_stats(self, snapshot: GlobalStatsSnapshot) -> None:
        """Registra estadísticas globales."""
        self.global_history["money"].append(snapshot.money)
        self.global_history["hunger"].append(snapshot.hunger)
        self.global_history["happiness"].append(snapshot.happiness)
        self.global_history["stress"].append(snapshot.stress)
        self.global_history["population"].append(snapshot.population)

        self.global_history["total_market_value"].append(snapshot.total_market_value)

        self.global_history["total_food"].append(snapshot.total_food)

        self.global_history["total_materials"].append(snapshot.total_materials)

        self.global_history["total_industrial"].append(snapshot.total_industrial)

        self.global_history["total_consumer"].append(snapshot.total_consumer)

        self.global_history["total_luxury"].append(snapshot.total_luxury)

        self.global_history["total_energy"].append(snapshot.total_energy)

        self.global_history["total_illegal"].append(snapshot.total_illegal)

    def record_world_resources(self, cities):

        totals = {resource_name: 0 for resource_name in RESOURCES}

        for city in cities:

            for resource, amount in city.resources.items():
                totals[resource] += amount

        for resource, amount in totals.items():
            self.resource_history[resource].append(amount)

    def calculate_global_stats(
        self,
        npcs: List[Any],
        cities: List[Any]
    ) -> GlobalStatsSnapshot:
        """
        Calcula estadísticas globales del mundo.
        """
    
        if not npcs:
            return GlobalStatsSnapshot(
                money=0,
                hunger=0,
                happiness=0,
                stress=0,
    
                population=0,
    
                total_market_value=0,
    
                total_food=0,
                total_materials=0,
                total_industrial=0,
                total_consumer=0,
                total_luxury=0,
                total_energy=0,
                total_illegal=0
            )
    
        population = len(npcs)
    
        total_market_value = sum(
            city.market_value
            for city in cities
        )
    
        total_food = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.FOOD
                ).values()
            )
            for city in cities
        )
    
        total_materials = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.MATERIAL
                ).values()
            )
            for city in cities
        )
    
        total_industrial = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.INDUSTRIAL
                ).values()
            )
            for city in cities
        )
    
        total_consumer = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.CONSUMER
                ).values()
            )
            for city in cities
        )
    
        total_luxury = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.LUXURY
                ).values()
            )
            for city in cities
        )
    
        total_energy = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.ENERGY
                ).values()
            )
            for city in cities
        )
    
        total_illegal = sum(
            sum(
                city.get_resources_by_category(
                    ResourceCategory.ILLEGAL
                ).values()
            )
            for city in cities
        )
    
        return GlobalStatsSnapshot(
            money=sum(n.money for n in npcs) / population,
            hunger=sum(n.hunger for n in npcs) / population,
            happiness=sum(n.happiness for n in npcs) / population,
            stress=sum(n.stress for n in npcs) / population,
    
            population=population,
    
            total_market_value=round(
                total_market_value,
                2
            ),
    
            total_food=total_food,
            total_materials=total_materials,
            total_industrial=total_industrial,
            total_consumer=total_consumer,
            total_luxury=total_luxury,
            total_energy=total_energy,
            total_illegal=total_illegal
        )

    def get_npc_history(self, npc_id: int) -> Dict[str, List[float]]:
        """Obtiene historial de un NPC específico."""
        return self.npc_history.get(npc_id, {})

    def get_global_history(self) -> Dict[str, List[float]]:
        """Obtiene historial global."""
        return self.global_history
