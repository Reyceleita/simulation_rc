"""
production_manager.py
Responsabilidad: Gestión de recursos, producción y bonificaciones.
"""

from typing import Dict, Any

from sim.core.City.config.city_resource_config import CITY_RESOURCE_CONFIG
from sim.core.resources.global_resources import RESOURCES


class ProductionManager:
    """
    Responsable de:
    - Almacenamiento de recursos (comida, bienes)
    - Cálculo de bonificaciones de producción según tipo de ciudad
    - Generación de recursos
    """

    def __init__(self, city_type: str):
        config = CITY_RESOURCE_CONFIG[city_type]

        self.resources = config["starting_resources"].copy()
        
        self.production_rates = config["production"]
        
        self.production_bonus = config["bonuses"]

        # # Bonificaciones según tipo de ciudad
        # if city_type == "agricultural":
        #     self.production_bonus = {
        #         "wheat": 2.5,
        #         "meat": 1.4
        #     }
        # elif city_type == "industrial":
        #     self.production_bonus = {
        #         "iron": 2.2,
        #         "tools": 1.8
        #     }

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

    def get_resources_by_category(self, category:str,) -> Dict[str, object]:
        
        result = {}
        
        for resource, amount in self.resources.items():
            data = RESOURCES.get(resource)
            
            if data and data.category == category:
                result[resource] = amount
        
        return result
    
    def update(self):
        for resource, base_amount in self.production_rates.items():
            
            produced = self.produce(resource, base_amount)

    def get_total_category_amount(self, category) -> float:
        total = 0
    
        resources = self.get_resources_by_category(category)
    
        for amount in resources.values():
            total += amount
    
        return total

    def get_total_market_value(self) -> float:
        total = 0

        for resource, amount in self.resources.items():

            definition = RESOURCES[resource]

            total += definition.base_price * amount

        return total