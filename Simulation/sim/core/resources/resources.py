from dataclasses import dataclass

from sim.core.resources.resources_types import ResourceCategory



@dataclass
class ResourceDefinition:
    name: str
    category: ResourceCategory

    base_price: float

    nutrition: float = 0
    durability: float = 0

    perishability: float = 0