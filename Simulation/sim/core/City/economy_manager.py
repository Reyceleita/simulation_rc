"""
economy_manager.py
Responsabilidad:
- Gestión económica de la ciudad
- Precios dinámicos
- Impuestos y subsidios
- Tesorería municipal
"""

from typing import Dict, List, Any

from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import ResourceCategory


class EconomyManager:
    """
    Responsable de:
    - Recaudación de impuestos
    - Distribución de subsidios
    - Ajuste dinámico de precios
    - Gestión de tesorería
    - Valor económico de recursos
    """

    # =====================================================
    # CONFIGURACIÓN ECONÓMICA
    # =====================================================

    TAX_DISTRIBUTION_RATE = 0.3

    MIN_PRICE_MULTIPLIER = 0.5
    MAX_PRICE_MULTIPLIER = 2.5

    DEFAULT_PRICE_SENSITIVITY = 0.4

    # Qué tan rápido cambian los precios
    PRICE_SMOOTHING = 0.1

    # =====================================================
    # INICIALIZACIÓN
    # =====================================================

    def __init__(self, economic_factor: float = 1.0):

        # Precios actuales dinámicos
        self.prices: Dict[str, float] = {
            resource_name: definition.base_price
            for resource_name, definition in RESOURCES.items()
        }

        # Factor económico general de ciudad
        self.economic_factor = economic_factor

        # Dinero municipal
        self.treasury: float = 0

    # =====================================================
    # IMPUESTOS
    # =====================================================

    def collect_taxes(self, npcs: List[Any]) -> float:
        """
        Distribuye subsidios desde la tesorería.

        Returns:
            Cantidad total distribuida
        """

        if not npcs:
            return 0.0

        subsidy = self.treasury * self.TAX_DISTRIBUTION_RATE
        per_npc = subsidy / len(npcs)

        for npc in npcs:
            npc.money += per_npc

        self.treasury -= subsidy

        return round(subsidy, 2)

    # =====================================================
    # AJUSTE DE PRECIOS
    # =====================================================

    def adjust_prices(
        self,
        resources: Dict[str, float],
        population: int
    ) -> None:
        """
        Ajusta precios dinámicamente según oferta/demanda.
        """

        for resource_name, current_supply in resources.items():

            definition = RESOURCES[resource_name]

            base_price = definition.base_price
            category = definition.category

            # =============================================
            # Sensibilidad según categoría
            # =============================================

            sensitivity = self.get_category_sensitivity(category)

            # =============================================
            # Oferta / demanda
            # =============================================

            ratio = current_supply / max(1, population)

            multiplier = max(
                self.MIN_PRICE_MULTIPLIER,
                min(
                    self.MAX_PRICE_MULTIPLIER,
                    2 - ratio * sensitivity
                )
            )

            # =============================================
            # Precio objetivo
            # =============================================

            target_price = (
                base_price
                * multiplier
                * self.economic_factor
            )

            # Evitar precios absurdamente bajos
            minimum_price = base_price * 0.3

            target_price = max(
                minimum_price,
                target_price
            )

            # =============================================
            # Inflación suave
            # =============================================

            current_price = self.prices[resource_name]

            new_price = current_price + (
                target_price - current_price
            ) * self.PRICE_SMOOTHING

            self.prices[resource_name] = round(
                new_price,
                2
            )

    # =====================================================
    # CONFIGURACIÓN POR CATEGORÍA
    # =====================================================

    def get_category_sensitivity(
        self,
        category: ResourceCategory
    ) -> float:
        """
        Qué tan sensible es una categoría a escasez.
        """

        if category == ResourceCategory.FOOD:
            return 0.7

        if category == ResourceCategory.LUXURY:
            return 0.2

        if category == ResourceCategory.ILLEGAL:
            return 1.0

        if category == ResourceCategory.ENERGY:
            return 0.8

        return self.DEFAULT_PRICE_SENSITIVITY

    # =====================================================
    # CONSULTAS
    # =====================================================

    def get_current_prices(self) -> Dict[str, float]:
        """Retorna precios actuales."""
        return self.prices.copy()

    def get_price(self, resource_name: str) -> float:
        """Retorna precio de un recurso."""
        return self.prices.get(resource_name, 0)

    def calculate_market_value(
        self,
        resources: Dict[str, float]
    ) -> float:
        """
        Calcula valor económico total de un inventario.
        """

        total = 0

        for resource_name, amount in resources.items():

            price = self.get_price(resource_name)

            total += price * amount

        return round(total, 2)

    # =====================================================
    # COMPRA / VENTA
    # =====================================================

    def buy_resource(
        self,
        resource_name: str,
        amount: float
    ) -> float:
        """
        Calcula costo de compra de un recurso.
        """

        return round(
            self.get_price(resource_name) * amount,
            2
        )

    def sell_resource(
        self,
        resource_name: str,
        amount: float
    ) -> float:
        """
        Calcula ganancia de venta.
        """

        return round(
            self.get_price(resource_name) * amount,
            2
        )

    # =====================================================
    # TESORERÍA
    # =====================================================

    def add_to_treasury(self, amount: float) -> None:
        """Agrega dinero a la tesorería."""

        self.treasury += amount

    def remove_from_treasury(self, amount: float) -> bool:
        """
        Retira dinero si hay suficiente.
        """

        if self.treasury >= amount:
            self.treasury -= amount
            return True

        return False

    def get_treasury(self) -> float:
        """Retorna balance municipal."""

        return round(self.treasury, 2)