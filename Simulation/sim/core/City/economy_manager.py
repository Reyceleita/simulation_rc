"""
economy_manager.py
Responsabilidad: Gestión económica de la ciudad — precios, impuestos, tesorería.
"""

from typing import Dict, List, Any


class EconomyManager:
    """
    Responsable de:
    - Recaudación de impuestos y distribución de subsidios
    - Ajuste dinámico de precios según oferta/demanda
    - Gestión de tesorería municipal
    """

    # Constantes de configuración
    TAX_DISTRIBUTION_RATE = 0.3
    MIN_PRICE_MULTIPLIER = 0.5
    MAX_PRICE_MULTIPLIER = 2.5
    PRICE_SENSITIVITY = 0.4

    def __init__(self, base_prices: Dict[str, int], economic_factor: float = 1.0):
        self.base_prices = base_prices.copy()
        self.cost_of_life = base_prices.copy()
        self.economic_factor = economic_factor
        self.treasury = 0

    def collect_taxes(self, npcs: List[Any]) -> float:
        """
        Recauda impuestos y distribuye subsidios entre la población.

        Args:
            npcs: Lista de NPCs residentes

        Returns:
            Monto total distribuido
        """
        if not npcs:
            return 0.0

        subsidy = self.treasury * self.TAX_DISTRIBUTION_RATE
        per_npc = subsidy / len(npcs)

        for npc in npcs:
            npc.money += per_npc

        self.treasury -= subsidy
        return subsidy

    def adjust_prices(self, food_supply: int, population: int) -> int:
        """
        Ajusta precios de comida según ratio oferta/demanda.

        Args:
            food_supply: Cantidad de comida disponible
            population: Población actual

        Returns:
            Nuevo precio de comida
        """
        ratio = food_supply / max(1, population)
        base_price = self.base_prices["food_price"]

        # Multiplier inversamente proporcional al ratio comida/población
        multiplier = max(
            self.MIN_PRICE_MULTIPLIER,
            min(self.MAX_PRICE_MULTIPLIER, 2 - ratio * self.PRICE_SENSITIVITY)
        )

        new_price = int(base_price * multiplier * self.economic_factor)
        self.cost_of_life["food_price"] = new_price

        return new_price

    def get_current_prices(self) -> Dict[str, int]:
        """Retorna precios actuales."""
        return self.cost_of_life.copy()

    def get_base_prices(self) -> Dict[str, int]:
        """Retorna precios base."""
        return self.base_prices.copy()

    def add_to_treasury(self, amount: float) -> None:
        """Agrega fondos a la tesorería."""
        self.treasury += amount

    def get_treasury(self) -> float:
        """Retorna balance de tesorería."""
        return self.treasury
