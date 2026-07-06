"""
trade_manager.py

Responsabilidad:
- Comercio entre ciudades
- Detección de escasez/excedente
- Generación de rutas comerciales
- Transferencia de recursos
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import (
    ResourceCategory
)


# =========================================================
# DATA CLASSES
# =========================================================

@dataclass
class TradeRoute:
    """
    Ruta comercial entre dos ciudades.
    """

    origin: Any
    destination: Any

    resource: str

    amount: float

    profit: float

    def __repr__(self) -> str:

        return (
            f"TradeRoute("
            f"{self.origin.name} -> "
            f"{self.destination.name}, "
            f"resource={self.resource}, "
            f"profit={self.profit:.2f}"
            f")"
        )


@dataclass
class TradeResult:
    """
    Resultado de una operación comercial.
    """

    success: bool

    resource: str

    amount: float

    price: float

    total_cost: float

    message: str = ""


# =========================================================
# TRADE MANAGER
# =========================================================

class TradeManager:

    """
    Responsable de:
    - Detectar necesidades
    - Detectar excedentes
    - Crear comercio automático
    - Ejecutar transferencias
    """

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    MIN_RESOURCE_RATIO = 2.0

    SURPLUS_THRESHOLD = 4.0

    MIN_PRICE_DIFF = 1.0

    TRANSPORT_COST = 2.0

    MIN_SELLER_RESERVE = 10

    MAX_TRANSFER_AMOUNT = 25

    # Prioridad de recursos
    RESOURCE_PRIORITY = {
        ResourceCategory.FOOD: 10,
        ResourceCategory.ENERGY: 9,
        ResourceCategory.INDUSTRIAL: 7,
        ResourceCategory.MATERIAL: 6,
        ResourceCategory.CONSUMER: 5,
        ResourceCategory.LUXURY: 2,
        ResourceCategory.ILLEGAL: 1
    }

    # =====================================================
    # INICIALIZACIÓN
    # =====================================================

    def __init__(self, logger: Any):

        self.logger = logger

        self.routes: List[TradeRoute] = []

    # =====================================================
    # RUTAS COMERCIALES
    # =====================================================

    def update_trade_routes(
        self,
        cities: List[Any]
    ) -> List[TradeRoute]:
        """
        Recalcula rutas comerciales.
        """

        self.routes = []

        for resource_name in RESOURCES.keys():

            for seller in cities:

                seller_surplus = self.get_resource_surplus(
                    seller,
                    resource_name
                )

                if seller_surplus <= 0:
                    continue

                for buyer in cities:

                    if seller == buyer:
                        continue

                    buyer_surplus = self.get_resource_surplus(
                        buyer,
                        resource_name
                    )

                    # Solo compradores con escasez
                    if buyer_surplus >= 0:
                        continue

                    seller_price = (
                        seller.economy.get_price(
                            resource_name
                        )
                    )

                    buyer_price = (
                        buyer.economy.get_price(
                            resource_name
                        )
                    )

                    price_diff = (
                        buyer_price
                        - seller_price
                    )

                    if price_diff < self.MIN_PRICE_DIFF:
                        continue

                    amount = min(
                        self.MAX_TRANSFER_AMOUNT,
                        seller.resources.get(
                            resource_name,
                            0
                        ) // 4
                    )

                    if amount <= 0:
                        continue

                    profit = (
                        (price_diff * amount)
                        - self.TRANSPORT_COST
                    )

                    self.routes.append(
                        TradeRoute(
                            origin=seller,
                            destination=buyer,
                            resource=resource_name,
                            amount=amount,
                            profit=profit
                        )
                    )

        # Más rentables primero
        self.routes.sort(
            key=lambda r: r.profit,
            reverse=True
        )

        return self.routes

    # =====================================================
    # NECESIDADES
    # =====================================================

    def get_resource_ratio(
        self,
        city: Any,
        resource_name: str
    ) -> float:
        """
        Ratio recurso/población.
        """

        amount = city.resources.get(
            resource_name,
            0
        )

        population = max(
            1,
            len(city.npcs)
        )

        return amount / population

    def get_resource_surplus(
        self,
        city: Any,
        resource_name: str
    ) -> float:
        """
        Excedente o escasez.

        Positivo:
            excedente

        Negativo:
            necesidad
        """

        ratio = self.get_resource_ratio(
            city,
            resource_name
        )

        ideal_ratio = self.MIN_RESOURCE_RATIO

        return ratio - ideal_ratio

    # =====================================================
    # VENDEDORES
    # =====================================================

    def find_best_seller(
        self,
        buyer: Any,
        resource_name: str,
        cities: List[Any]
    ) -> Optional[Any]:
        """
        Encuentra mejor vendedor.
        """

        best = None

        best_price = float("inf")

        for seller in cities:

            if seller == buyer:
                continue

            surplus = self.get_resource_surplus(
                seller,
                resource_name
            )

            if surplus <= 0:
                continue

            available = seller.resources.get(
                resource_name,
                0
            )

            if available < self.MIN_SELLER_RESERVE:
                continue

            price = (
                seller.economy.get_price(
                    resource_name
                )
                + self.TRANSPORT_COST
            )

            if price < best_price:

                best_price = price

                best = seller

        return best

    # =====================================================
    # COMERCIO
    # =====================================================

    def execute_trade(
        self,
        buyer: Any,
        seller: Any,
        resource_name: str
    ) -> TradeResult:
        """
        Ejecuta transacción comercial.
        """

        seller_amount = seller.resources.get(
            resource_name,
            0
        )

        if seller_amount < self.MIN_SELLER_RESERVE:

            return TradeResult(
                False,
                resource_name,
                0,
                0,
                0,
                "Reservas insuficientes"
            )

        amount = min(
            self.MAX_TRANSFER_AMOUNT,
            seller_amount // 4
        )

        if amount <= 0:

            return TradeResult(
                False,
                resource_name,
                0,
                0,
                0,
                "Cantidad insuficiente"
            )

        price = (
            seller.economy.get_price(
                resource_name
            )
            + self.TRANSPORT_COST
        )

        total_cost = price * amount

        buyer_money = sum(
            npc.money
            for npc in buyer.npcs
        )

        # Ajustar compra al dinero disponible
        if buyer_money < total_cost:

            amount = int(
                buyer_money / price
            )

            total_cost = (
                amount * price
            )

            if amount <= 0:

                return TradeResult(
                    False,
                    resource_name,
                    0,
                    0,
                    0,
                    "Fondos insuficientes"
                )

        # =================================================
        # TRANSFERENCIA
        # =================================================

        seller.consume_resource(
            resource_name,
            amount
        )

        buyer.add_resource(
            resource_name,
            amount
        )

        # =================================================
        # DINERO
        # =================================================

        if buyer.npcs:

            cost_per_npc = (
                total_cost
                / len(buyer.npcs)
            )

            for npc in buyer.npcs:
                npc.money -= cost_per_npc

        if seller.npcs:

            income_per_npc = (
                total_cost
                / len(seller.npcs)
            )

            for npc in seller.npcs:
                npc.money += income_per_npc

        # =================================================
        # REGISTRO
        # =================================================

        self.logger.log(
            f"Comercio: "
            f"{seller.name} -> "
            f"{buyer.name} | "
            f"{amount} {resource_name}"
        )

        return TradeResult(
            success=True,
            resource=resource_name,
            amount=amount,
            price=price,
            total_cost=round(
                total_cost,
                2
            )
        )

    # =====================================================
    # CICLO GLOBAL
    # =====================================================

    def trade_between_cities(
        self,
        cities: List[Any]
    ) -> List[TradeResult]:
        """
        Ejecuta comercio global.
        """

        results = []

        for buyer in cities:

            for resource_name in RESOURCES.keys():

                surplus = self.get_resource_surplus(
                    buyer,
                    resource_name
                )

                # Solo recursos escasos
                if surplus >= 0:
                    continue

                seller = self.find_best_seller(
                    buyer,
                    resource_name,
                    cities
                )

                if not seller:
                    continue

                result = self.execute_trade(
                    buyer,
                    seller,
                    resource_name
                )

                results.append(result)

        return results

    # =====================================================
    # DEBUG
    # =====================================================

    def get_route_summary(self) -> str:
        """
        Resumen de rutas comerciales.
        """

        if not self.routes:
            return "Sin rutas comerciales activas"

        lines = [
            "Rutas comerciales activas:"
        ]

        for route in self.routes:

            lines.append(
                f"  {route.origin.name} -> "
                f"{route.destination.name} | "
                f"{route.resource} | "
                f"profit={route.profit:.2f}"
            )

        return "\n".join(lines)