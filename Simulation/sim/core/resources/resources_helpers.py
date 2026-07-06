from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources import ResourceDefinition
from sim.core.resources.resources_types import ResourceCategory


def get_resource_definition(resource_name: str) -> ResourceDefinition:
    return RESOURCES[resource_name]

def is_food(resource_name: str) -> bool:
    return (
        RESOURCES[resource_name].category
        == ResourceCategory.FOOD
    )
