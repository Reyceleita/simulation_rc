"""
city.py

Responsabilidad:
- Orquestación de subsistemas de ciudad
- Coordinación de economía, producción y métricas sociales
- Interfaz principal de interacción con la ciudad
"""

from typing import Dict, List, Any

from sim.core.City.location import Location
from sim.core.City.location_registry import LocationType
from sim.core.resources.resources_types import ResourceCategory

from sim.core.City.economy_manager import EconomyManager
from sim.core.City.production_manager import ProductionManager
from sim.core.City.history_recorder import (
    HistoryRecorder,
    CitySnapshot
)
from sim.core.City.social_metrics import (
    SocialMetricsCalculator
)

CITY_POSITIONS = {

    "Lati": {
        "x": 900,
        "y": 600,
    },

    "Causland": {
        "x": 1280,
        "y": 1500,
    },

    "Solstadia": {
        "x": 580,
        "y": 1200,
    },

    "Alokla": {
        "x": 2050,
        "y": 1345,
    },

}

CITY_MAP = {

    "Lati": "Lati.png",

    "Causland": "Causland.png",

    "Solstadia": "Solstadia.png",

    "Alokla": "Alokla.png",

}

CITY_LOCATIONS = {
    "Lati": {
        
            LocationType.RESIDENTIAL:
        
                Location(
                    "home",
                    "Barrio",
                    LocationType.RESIDENTIAL,
                    {"x":850,"y":400}
                ),
        
            LocationType.WORK:
        
                Location(
                    "work",
                    "Trabajo",
                    LocationType.WORK,
                    {"x":300,"y":600}
                ),
        
            LocationType.SHOPPING:
        
                Location(
                    "shop",
                    "Mercado",
                    LocationType.SHOPPING,
                    {"x":600,"y":370}
                ),
        
        },
    "Causland": {
        
            LocationType.RESIDENTIAL:
        
                Location(
                    "home",
                    "Barrio",
                    LocationType.RESIDENTIAL,
                    {"x":300,"y":300}
                ),
        
            LocationType.WORK:
        
                Location(
                    "work",
                    "Trabajo",
                    LocationType.WORK,
                    {"x":600,"y":750}
                ),
        
            LocationType.SHOPPING:
        
                Location(
                    "shop",
                    "Mercado",
                    LocationType.SHOPPING,
                    {"x":700,"y":450}
                ),
        
        },
    "Solstadia": {
        
            LocationType.RESIDENTIAL:
        
                Location(
                    "home",
                    "Barrio",
                    LocationType.RESIDENTIAL,
                    {"x":550,"y":200}
                ),
        
            LocationType.WORK:
        
                Location(
                    "work",
                    "Trabajo",
                    LocationType.WORK,
                    {"x":850,"y":550}
                ),
        
            LocationType.SHOPPING:
        
                Location(
                    "shop",
                    "Mercado",
                    LocationType.SHOPPING,
                    {"x":550,"y":385}
                ),
        
        },
    "Alokla": {
        
            LocationType.RESIDENTIAL:
        
                Location(
                    "home",
                    "Barrio",
                    LocationType.RESIDENTIAL,
                    {"x":250,"y":400}
                ),
        
            LocationType.WORK:
        
                Location(
                    "work",
                    "Trabajo",
                    LocationType.WORK,
                    {"x":900,"y":350}
                ),
        
            LocationType.SHOPPING:
        
                Location(
                    "shop",
                    "Mercado",
                    LocationType.SHOPPING,
                    {"x":680,"y":450}
                ),
        
        }
}

class City:
    """
    Orquestador principal de una ciudad.

    Responsabilidades:
    - Mantener identidad/configuración
    - Coordinar subsistemas
    - Exponer interfaz unificada

    NO implementa lógica económica directamente.
    """

    # =====================================================
    # INICIALIZACIÓN
    # =====================================================

    def __init__(
        self,
        config: Dict,
        name: str = "City"
    ):

        # =================================================
        # IDENTIDAD
        # =================================================

        self.name = name
        self.type = config["type"]

        self.culture = config["culture"]
        self.base_stress = config["base_stress"]
        self.position  = CITY_POSITIONS[self.name]
        self.map = CITY_MAP[self.name]

        # =================================================
        # Locaciones
        # =================================================

        self.locations = CITY_LOCATIONS[self.name]

        # =================================================
        # POBLACIÓN
        # =================================================

        self.npcs: List[Any] = []

        # Distribución laboral
        self.jobs_distribution = config["jobs"]

        # =================================================
        # COMERCIO
        # =================================================

        self.imports: Dict[str, float] = {}
        self.exports: Dict[str, float] = {}

        # =================================================
        # SUBSISTEMAS
        # =================================================

        self.economy = EconomyManager(
            economic_factor=config.get(
                "economic_factor",
                1.0
            )
        )

        self.production = ProductionManager(
            city_type=self.type
        )

        self.history = HistoryRecorder()

        self.social = SocialMetricsCalculator()

    # =====================================================
    # PROPIEDADES
    # =====================================================
    
    
    @property
    def map_data(self):
    
        return {
        
            "name": self.name,
    
            "type": self.type,
    
            "population": len(self.npcs),
    
            "position": self.position,
    
        }

    @property
    def resources(self) -> Dict[str, float]:
        """Retorna recursos actuales."""
        return self.production.get_all_resources()

    @property
    def prices(self) -> Dict[str, float]:
        """Retorna precios actuales."""
        return self.economy.get_current_prices()

    @property
    def treasury(self) -> float:
        """Retorna tesorería municipal."""
        return self.economy.get_treasury()

    @property
    def market_value(self) -> float:
        """
        Valor económico total del inventario.
        """

        return self.economy.calculate_market_value(
            self.resources
        )

    @property
    def food_supply(self) -> float:
        """
        Cantidad total de comida disponible.
        """

        return self.production.get_total_category_amount(
            ResourceCategory.FOOD
        )

    @property
    def wealth(self) -> float:
        """
        Riqueza total de ciudad.
        """

        npc_money = sum(
            npc.money
            for npc in self.npcs
        )

        return round(
            npc_money
            + self.market_value
            + self.treasury,
            2
        )

    # =====================================================
    # ACTUALIZACIÓN
    # =====================================================

    def update(self) -> None:
        """
        Ciclo principal de actualización.
        """

        # =================================================
        # 1. PRODUCCIÓN
        # =================================================

        self.production.update()

        # =================================================
        # 2. ECONOMÍA
        # =================================================

        self.economy.collect_taxes(
            self.npcs
        )

        self.economy.adjust_prices(
            self.resources,
            len(self.npcs)
        )

        # =================================================
        # 3. MÉTRICAS SOCIALES
        # =================================================

        social = self.social.calculate(
            self.npcs
        )

        employment = (
            self.social.get_employment_stats(
                self.npcs
            )
        )

        # =================================================
        # 4. HISTORIAL
        # =================================================

        snapshot = CitySnapshot(
            food=self.food_supply,
            population=len(self.npcs),
            employed=employment["employed"],
            unemployed=employment["unemployed"],
            food_price=self.prices.get("wheat", 1),  # o el alimento base
        
            avg_hunger=social.avg_hunger,
            avg_money=social.avg_money,
            avg_stress=social.avg_stress,
            avg_happiness=social.avg_happiness
        )

        self.history.record(snapshot)

    # =====================================================
    # RECURSOS
    # =====================================================

    def add_resource(
        self,
        resource_type: str,
        amount: float
    ) -> None:
        """
        Agrega recurso al inventario.
        """

        self.production.add_resource(
            resource_type,
            amount
        )

    def consume_resource(
        self,
        resource_type: str,
        amount: float
    ) -> bool:
        """
        Consume recurso del inventario.
        """

        return self.production.consume_resource(
            resource_type,
            amount
        )

    def consume_food(
        self,
        amount: float
    ) -> bool:
        """
        Consume comida usando múltiples recursos.
        """

        foods = self.get_resources_by_category(
            ResourceCategory.FOOD
        )

        remaining = amount

        for resource_name, quantity in foods.items():

            if remaining <= 0:
                break

            consumed = min(
                quantity,
                remaining
            )

            self.consume_resource(
                resource_name,
                consumed
            )

            remaining -= consumed

        return remaining <= 0

    def get_resources_by_category(
        self,
        category: ResourceCategory
    ) -> Dict[str, float]:
        """
        Retorna recursos de una categoría.
        """

        return self.production.get_resources_by_category(
            category
        )

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def get_employment_stats(
        self
    ) -> Dict[str, int]:
        """
        Estadísticas laborales.
        """

        return self.social.get_employment_stats(
            self.npcs
        )

    def get_social_metrics(self):
        """
        Métricas sociales actuales.
        """

        return self.social.calculate(
            self.npcs
        )

    # =====================================================
    # HISTORIAL
    # =====================================================

    def get_history(
        self,
        metric: str = None
    ):
        """
        Retorna historial completo o métrica específica.
        """

        if metric:
            return self.history.get_history(metric)

        return self.history.get_all_history()

    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"City("
            f"{self.name}, "
            f"type={self.type}, "
            f"pop={len(self.npcs)}"
            f")"
        )