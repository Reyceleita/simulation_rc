"""
world.py
Responsabilidad: Orquestación principal del mundo.
Coordina todos los subsistemas pero NO implementa lógica específica.
"""

import random
import threading
from typing import Dict, List

from sim.core.Npc.npc import NPC
from sim.core.City.city_refactored import City
from sim.generators.npc_generator import NPCGenerator
from sim.utils.logger import Logger
from cities import *
from professions import PROFESSIONS

from sim.core.World.time_manager import TimeManager
from sim.core.World.stats_tracker import StatsTracker, NPCStatsSnapshot, GlobalStatsSnapshot
from sim.core.World.job_manager import JobManager
from sim.core.World.trade_manager import TradeManager
from sim.core.World.population_manager import PopulationManager 
from sim.tracking.decision_tracker import DecisionTracker
from sim.tracking.event_tracker import EventTracker


class World:
    """
    Orquestador principal del mundo.

    Responsabilidades:
    - Inicializar y coordinar subsistemas
    - Ejecutar ciclo de update
    - Delegar operaciones especializadas a managers
    """

    def __init__(self):
        # Lock para concurrencia
        self.lock = threading.Lock()

        # Logger compartido
        self.logger = Logger()

        # ========== SUBSISTEMAS ==========
        self.time_manager = TimeManager(start_hour=6, start_day=1)
        self.stats_tracker = StatsTracker()
        self.job_manager = JobManager(PROFESSIONS)
        self.trade_manager = TradeManager(self.logger)
        self.population_manager = PopulationManager(NPCGenerator())
        self.decision_tracker = DecisionTracker()
        self.event_tracker = EventTracker()

        # ========== CIUDADES ==========
        self.cities = [
            City(agricultural_config, "Agro"),
            City(industrial_config, "Indus"),
            City(commercial_config, "Comer"),
            City(marginal_config, "Marginal")
        ]

        self.city_population = {
            "Agro": 25,
            "Indus": 25,
            "Comer": 25,
            "Marginal": 25
        }

        # ========== NPCs ==========
        self.npcs = self.population_manager.generate_population(
            self.cities, 
            self.city_population
        )

        # ========== INICIALIZACIÓN ==========
        # Asignar trabajos
        for city in self.cities:
            self.job_manager.assign_jobs(city)

        # Inicializar relaciones
        self.population_manager.initialize_relationships(self.npcs)

        # Registrar NPCs en tracker
        for npc in self.npcs:
            self.stats_tracker.register_npc(npc.id)

        # ========== ESTADO DE SIMULACIÓN ==========
        self.busy_npcs: set = set()
        
        # ========== EVENTOS ==========
        #self.tick_event = []

    def update(self) -> None:
        """
        Ciclo principal de actualización del mundo.
        Orquesta la ejecución de todos los subsistemas en orden.
        """
        # 1. Avanzar tiempo
        self.time_manager.advance()
        
        # 2. Limpiar eventos
        self.event_tracker.clear_tick()

        # 3. Actualizar rutas comerciales
        self.trade_manager.update_trade_routes(self.cities)

        # 4. Ejecutar comercio entre ciudades
        self.trade_manager.trade_between_cities(self.cities)

        # 5. Mezclar orden de NPCs para fairness
        random.shuffle(self.npcs)

        # 6. Logging de inicio de tick
        self.logger.log(
            f"\n--- TICK {self.time_manager.tick} | "
            f"{self.time_manager.get_time_string()} ---"
        )

        # 7. Resetear NPCs ocupados
        self.busy_npcs = set()

        # 8. Calcular y registrar estadísticas globales
        global_stats = self.stats_tracker.calculate_global_averages(self.npcs)

        with self.lock:
            self.stats_tracker.record_global_stats(global_stats)

        # 9. Actualizar cada NPC
        for npc in self.npcs:
            if npc.id in self.busy_npcs:
                continue

            npc.update(self)

            # Registrar estadísticas del NPC
            snapshot = NPCStatsSnapshot(
                money=npc.money,
                hunger=npc.hunger,
                happiness=npc.happiness,
                stress=npc.stress
            )
            self.stats_tracker.record_npc_stats(npc.id, snapshot)

        # 10. Actualizar ciudades
        for city in self.cities:
            city.update()

        # 11. Mostrar estadísticas
        self._show_stats()

    def _show_stats(self) -> None:
        """Muestra estadísticas actuales del mundo."""
        total_money = self.population_manager.get_total_money(self.npcs)
        avg_hunger = sum(n.hunger for n in self.npcs) / max(1, len(self.npcs))

        self.logger.log(f"NPC's: {len(self.npcs)}")
        self.logger.log(f"Dinero total: {total_money}")
        self.logger.log(f"Hambre promedio: {avg_hunger:.2f}")

        for city in self.cities:
            workers = self.job_manager.count_workers(city)
            unemployed = self.job_manager.count_unemployed(city)

            self.logger.log(
                f"{city.name} | "
                f"Población: {len(city.npcs)} | "
                f"Trabajan: {workers} | "
                f"Desempleados: {unemployed}"
            )

    def get_stats_history(self) -> Dict[str, List[float]]:
        """Retorna historial global de estadísticas."""
        return self.stats_tracker.get_global_history()

    def get_npc_history(self, npc_id: int) -> Dict[str, List[float]]:
        """Retorna historial de un NPC específico."""
        return self.stats_tracker.get_npc_history(npc_id)

    def get_trade_routes(self) -> List:
        """Retorna rutas comerciales activas."""
        return self.trade_manager.routes
