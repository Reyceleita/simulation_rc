"""
trade_manager.py
Responsabilidad: Lógica de comercio entre ciudades.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TradeRoute:
    """Representa una ruta comercial entre dos ciudades."""
    origin: Any  # City
    destination: Any  # City
    profit: float

    def __repr__(self) -> str:
        return f"TradeRoute({self.origin.name} -> {self.destination.name}, profit={self.profit:.2f})"


@dataclass
class TradeResult:
    """Resultado de una transacción comercial."""
    success: bool
    amount: int
    price: float
    total_cost: float
    message: str = ""


class TradeManager:
    """
    Responsable de:
    - Identificar ciudades compradoras y vendedoras
    - Calcular rutas comerciales óptimas
    - Ejecutar transacciones de comida
    - Registrar operaciones comerciales
    """

    # Constantes de configuración
    MIN_SELLER_RATIO = 3.0
    MAX_BUYER_RATIO = 1.5
    MIN_PRICE_DIFF = 3.0
    TRANSPORT_COST = 2.0
    MIN_SELLER_FOOD = 20
    MIN_SELLER_RESERVE = 10
    MAX_BUYER_FOOD = 150
    MAX_TRANSFER_AMOUNT = 20
    FOOD_PRESSURE_THRESHOLD = 50

    def __init__(self, logger: Any):
        self.logger = logger
        self.routes: List[TradeRoute] = []

    def update_trade_routes(self, cities: List[Any]) -> List[TradeRoute]:
        """
        Recalcula rutas comerciales basadas en diferencias de precio y presión alimentaria.

        Args:
            cities: Lista de ciudades

        Returns:
            Lista de rutas comerciales viables
        """
        self.routes = []

        for city_a in cities:
            for city_b in cities:
                if city_a == city_b:
                    continue

                price_diff = (
                    city_b.cost_of_life["food_price"] - 
                    city_a.cost_of_life["food_price"]
                )

                food_pressure = max(0, self.FOOD_PRESSURE_THRESHOLD - city_b.resources["food"])

                profit = price_diff + food_pressure * 0.5

                if price_diff > self.MIN_PRICE_DIFF:
                    self.routes.append(TradeRoute(city_a, city_b, profit))

        return self.routes

    def classify_cities(self, cities: List[Any]) -> Tuple[List[Any], List[Any]]:
        """
        Clasifica ciudades en compradoras y vendedoras según ratio comida/población.

        Returns:
            Tupla (compradores, vendedores)
        """
        buyers = []
        sellers = []

        for city in cities:
            ratio = self._get_food_ratio(city)

            if ratio < self.MAX_BUYER_RATIO:
                buyers.append(city)
            elif ratio > self.MIN_SELLER_RATIO:
                sellers.append(city)

        return buyers, sellers

    def _get_food_ratio(self, city: Any) -> float:
        """Calcula ratio comida/población de una ciudad."""
        population = max(1, len(city.npcs))
        return city.resources["food"] / population

    def find_best_seller(self, buyer: Any, sellers: List[Any]) -> Optional[Any]:
        """
        Encuentra el mejor vendedor para una ciudad compradora.

        Args:
            buyer: Ciudad compradora
            sellers: Lista de ciudades vendedoras candidatas

        Returns:
            Mejor ciudad vendedora o None
        """
        best = None
        best_price = float("inf")

        for seller in sellers:
            if seller == buyer:
                continue

            price = seller.cost_of_life["food_price"] + self.TRANSPORT_COST

            if price < best_price and seller.resources["food"] > self.MIN_SELLER_FOOD:
                best_price = price
                best = seller

        return best

    def execute_trade(self, buyer: Any, seller: Any) -> TradeResult:
        """
        Ejecuta una transacción comercial de comida entre dos ciudades.

        Args:
            buyer: Ciudad compradora
            seller: Ciudad vendedora

        Returns:
            Resultado de la transacción
        """
        # Validaciones básicas
        if seller.resources['food'] < self.MIN_SELLER_RESERVE:
            return TradeResult(False, 0, 0, 0, "Vendedor sin reservas suficientes")

        if buyer.resources['food'] > self.MAX_BUYER_FOOD:
            return TradeResult(False, 0, 0, 0, "Comprador con reservas llenas")

        # Calcular cantidad a transferir
        amount = min(self.MAX_TRANSFER_AMOUNT, seller.resources['food'] // 4)

        if amount <= 0:
            return TradeResult(False, 0, 0, 0, "Cantidad insuficiente")

        # Calcular precio
        price = seller.cost_of_life['food_price'] + self.TRANSPORT_COST

        # Verificar capacidad de pago del comprador
        total_money = sum(n.money for n in buyer.npcs)

        if total_money < price * amount:
            # Comprar menos en vez de cancelar
            amount = int(total_money / price)
            if amount <= 0:
                return TradeResult(False, 0, 0, 0, "Fondos insuficientes")

        # Ejecutar transferencia
        seller.resources['food'] -= amount
        buyer.resources['food'] += amount

        # Transferir dinero (distribuido entre NPCs)
        total_cost = price * amount
        cost_per_npc = total_cost / len(buyer.npcs)
        income_per_npc = total_cost / len(seller.npcs)

        for npc in buyer.npcs:
            npc.money -= cost_per_npc

        for npc in seller.npcs:
            npc.money += income_per_npc

        # Registrar
        self.logger.log(f"Comercio: {seller.name} -> {buyer.name} | {amount} comida")

        return TradeResult(True, amount, price, total_cost)

    def trade_between_cities(self, cities: List[Any]) -> List[TradeResult]:
        """
        Ejecuta todas las transacciones comerciales posibles entre ciudades.

        Args:
            cities: Lista de ciudades

        Returns:
            Lista de resultados de transacciones
        """
        results = []
        buyers, sellers = self.classify_cities(cities)

        for buyer in buyers:
            seller = self.find_best_seller(buyer, sellers)

            if not seller:
                continue

            result = self.execute_trade(buyer, seller)
            results.append(result)

        return results

    def get_route_summary(self) -> str:
        """Retorna resumen de rutas comerciales activas."""
        if not self.routes:
            return "Sin rutas comerciales activas"

        lines = ["Rutas comerciales activas:"]
        for route in self.routes:
            lines.append(f"  {route}")
        return "\n".join(lines)
