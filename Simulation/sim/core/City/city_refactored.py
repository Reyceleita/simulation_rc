"""
city.py
Responsabilidad: Orquestación de subsistemas de una ciudad.
Coordina economía, producción, historial y métricas sociales.
"""

from typing import Dict, List, Any

from sim.core.City.economy_manager import EconomyManager
from sim.core.City.production_manager import ProductionManager
from sim.core.City.history_recorder import HistoryRecorder, CitySnapshot
from sim.core.City.social_metrics import SocialMetricsCalculator


class City:
    """
    Orquestador de una ciudad.

    Responsabilidades:
    - Mantener identidad y configuración de la ciudad
    - Coordinar actualización de subsistemas
    - Proveer interfaz unificada para consultas

    NO implementa lógica de negocio — delega a managers especializados.
    """

    def __init__(self, config: Dict, name: str = "City"):
        # Identidad
        self.name = name
        self.type = config["type"]
        self.culture = config["culture"]
        self.base_stress = config["base_stress"]

        # Población
        self.npcs: List[Any] = []

        # Empleo (configuración, no lógica)
        self.jobs_distribution = config["jobs"]

        # ========== SUBSISTEMAS ==========
        self.economy = EconomyManager(
            base_prices=config["cost_of_life"],
            economic_factor=config.get("economic_factor", 1.0)
        )

        self.production = ProductionManager(city_type=self.type)

        self.history = HistoryRecorder()

        self.social = SocialMetricsCalculator()

    @property
    def resources(self) -> Dict[str, float]:
        """Proxy a recursos del production manager."""
        return self.production.get_all_resources()

    @property
    def cost_of_life(self) -> Dict[str, int]:
        """Proxy a precios del economy manager."""
        return self.economy.get_current_prices()

    @property
    def treasury(self) -> float:
        """Proxy a tesorería del economy manager."""
        return self.economy.get_treasury()

    def update(self) -> None:
        """
        Ciclo de actualización de la ciudad.
        Orquesta la ejecución de todos los subsistemas.
        """
        # 1. Recaudar impuestos y distribuir
        self.economy.collect_taxes(self.npcs)

        # 2. Ajustar precios según oferta/demanda
        food_supply = self.production.get_resource("food")
        self.economy.adjust_prices(food_supply, len(self.npcs))

        # 3. Calcular métricas sociales
        social = self.social.calculate(self.npcs)
        employment = self.social.get_employment_stats(self.npcs)

        # 4. Registrar historial
        snapshot = CitySnapshot(
            food=food_supply,
            population=len(self.npcs),
            employed=employment["employed"],
            unemployed=employment["unemployed"],
            food_price=self.economy.get_current_prices()["food_price"],
            avg_hunger=social.avg_hunger,
            avg_money=social.avg_money,
            avg_stress=social.avg_stress,
            avg_happiness=social.avg_happiness
        )
        self.history.record(snapshot)

    def get_employment_stats(self) -> Dict[str, int]:
        """Retorna estadísticas de empleo."""
        return self.social.get_employment_stats(self.npcs)

    def get_social_metrics(self):
        """Retorna métricas sociales actuales."""
        return self.social.calculate(self.npcs)

    def get_history(self, metric: str = None):
        """
        Retorna historial de métricas.

        Args:
            metric: Nombre de métrica específica, o None para todo
        """
        if metric:
            return self.history.get_history(metric)
        return self.history.get_all_history()

    def add_resource(self, resource_type: str, amount: float) -> None:
        """Agrega recurso a la ciudad."""
        self.production.add_resource(resource_type, amount)

    def consume_resource(self, resource_type: str, amount: float) -> bool:
        """Consume recurso de la ciudad."""
        return self.production.consume_resource(resource_type, amount)

    def __repr__(self) -> str:
        return f"City({self.name}, type={self.type}, pop={len(self.npcs)})"
