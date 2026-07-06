from sim.core.resources.global_resources import RESOURCES


def get_category_stock(npc, category):
    total = 0

    for resource_name, amount in npc.inventory.items():

        definition = RESOURCES.get(resource_name)

        if definition and definition.category == category:
            total += amount

    return total


def get_inventory_value(npc):

    value = 0

    for resource_name, amount in npc.inventory.items():

        definition = RESOURCES.get(resource_name)

        if definition:
            value += definition.base_price * amount

    return value