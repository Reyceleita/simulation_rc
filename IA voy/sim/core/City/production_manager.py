"""
production_manager.py
Responsabilidad: Gestión de recursos, producción y bonificaciones.
"""

from typing import Dict, Any


class ProductionManager:
    """
    Responsable de:
    - Almacenamiento de recursos (comida, bienes)
    - Cálculo de bonificaciones de producción según tipo de ciudad
    - Generación de recursos
    """

    def __init__(self, city_type: str):
        self.resources: Dict[str, float] = {
            "food": 200
        }

        # Bonificaciones según tipo de ciudad
        self.production_bonus = {
            "food": 2.5 if city_type == "agricultural" else 0.8,
            "goods": 1.5 if city_type == "industrial" else 0.7
        }

    def add_resource(self, resource_type: str, amount: float) -> None:
        """Agrega recurso al almacén."""
        self.resources[resource_type] = self.resources.get(resource_type, 0) + amount

    def consume_resource(self, resource_type: str, amount: float) -> bool:
        """
        Consume recurso si hay suficiente.

        Returns:
            True si se pudo consumir, False si no había suficiente
        """
        current = self.resources.get(resource_type, 0)
        if current >= amount:
            self.resources[resource_type] = current - amount
            return True
        return False

    def get_resource(self, resource_type: str) -> float:
        """Retorna cantidad de un recurso."""
        return self.resources.get(resource_type, 0)

    def get_all_resources(self) -> Dict[str, float]:
        """Retorna todos los recursos."""
        return self.resources.copy()

    def get_production_bonus(self, resource_type: str) -> float:
        """Retorna bonus de producción para un recurso."""
        return self.production_bonus.get(resource_type, 1.0)

    def produce(self, resource_type: str, base_amount: float) -> float:
        """
        Produce recurso aplicando bonus de la ciudad.

        Returns:
            Cantidad real producida
        """
        bonus = self.get_production_bonus(resource_type)
        actual = base_amount * bonus
        self.add_resource(resource_type, actual)
        return actual
