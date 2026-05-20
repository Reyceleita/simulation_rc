"""
population_manager.py
Responsabilidad: Gestión de población, generación de NPCs y relaciones.
"""

import random
from typing import List, Dict, Any, Optional


class PopulationManager:
    """
    Responsable de:
    - Generar población inicial
    - Distribuir NPCs entre ciudades
    - Inicializar relaciones entre NPCs
    """

    def __init__(self, npc_generator: Any):
        self.generator = npc_generator
        self._npc_counter = 0

    def generate_population(
        self, 
        cities: List[Any], 
        city_population: Dict[str, int]
    ) -> List[Any]:
        """
        Genera población inicial distribuida entre ciudades.

        Args:
            cities: Lista de ciudades
            city_population: Diccionario {nombre_ciudad: cantidad}

        Returns:
            Lista de todos los NPCs generados
        """
        all_npcs = []

        for city in cities:
            target = city_population.get(city.name, 0)

            for _ in range(target):
                npc = self.generator.create_npc(self._npc_counter)
                npc.city = city
                city.npcs.append(npc)
                all_npcs.append(npc)
                self._npc_counter += 1

        return all_npcs

    def initialize_relationships(self, npcs: List[Any]) -> None:
        """
        Inicializa relaciones aleatorias entre todos los pares de NPCs.

        Args:
            npcs: Lista de NPCs
        """
        for npc in npcs:
            for other in npcs:
                if npc.id != other.id:
                    npc.social.relationships[other.id] = random.uniform(-0.2, 0.2)

    def get_total_population(self, cities: List[Any]) -> int:
        """Cuenta población total."""
        return sum(len(c.npcs) for c in cities)

    def get_city_population(self, city: Any) -> int:
        """Cuenta población de una ciudad."""
        return len(city.npcs)

    def get_npc_by_id(self, npcs: List[Any], npc_id: int) -> Optional[Any]:
        """Busca NPC por ID."""
        for npc in npcs:
            if npc.id == npc_id:
                return npc
        return None

    def get_average_money(self, npcs: List[Any]) -> float:
        """Calcula dinero promedio."""
        if not npcs:
            return 0.0
        return sum(n.money for n in npcs) / len(npcs)

    def get_total_money(self, npcs: List[Any]) -> float:
        """Calcula dinero total."""
        return sum(n.money for n in npcs)
