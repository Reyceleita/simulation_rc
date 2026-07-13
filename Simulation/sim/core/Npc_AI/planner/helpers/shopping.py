"""
shopping.py

Funciones auxiliares para que el Planner decida qué recursos comprar.

Este módulo NO realiza compras.
Únicamente analiza el mercado y devuelve recomendaciones.
"""

from sim.core.resources.global_resources import RESOURCES
from sim.core.resources.resources_types import ResourceCategory


# -------------------------------------------------------------
# Selección de recursos
# -------------------------------------------------------------

def choose_resource(npc, category: ResourceCategory):
    """
    Devuelve el mejor recurso de una categoría para comprar.

    Actualmente utiliza el recurso más barato disponible.

    Parameters
    ----------
    npc : NPC

    category : ResourceCategory

    Returns
    -------
    str | None
    """

    market = npc.city.get_resources_by_category(category)

    cheapest = None
    cheapest_price = float("inf")

    for resource, stock in market.items():

        if stock <= 0:
            continue

        price = npc.city.prices.get(resource)

        if price is None:
            continue

        if price < cheapest_price:

            cheapest = resource
            cheapest_price = price

    return cheapest


# -------------------------------------------------------------
# Cantidad
# -------------------------------------------------------------

def calculate_amount(
    npc,
    resource: str
):
    """
    Decide cuántas unidades comprar.

    En el futuro este cálculo puede tener en cuenta:

        - dinero
        - hambre
        - stock del inventario
        - personalidad
        - inflación
        - tamaño familiar
        - etc.
    """

    definition = RESOURCES.get(resource)

    if definition is None:
        return 0

    category = definition.category

    if category == ResourceCategory.FOOD:

        if npc.money < 20:
            return 1

        if npc.hunger > 80:
            return 5

        return 3

    if category == ResourceCategory.CONSUMER_GOODS:

        if npc.money < 50:
            return 1

        return 2

    if category == ResourceCategory.LUXURY:

        if npc.money < 150:
            return 1

        return 2

    return 1


# -------------------------------------------------------------
# Coste
# -------------------------------------------------------------

def calculate_cost(
    city,
    resource,
    amount
):

    price = city.prices.get(resource)

    if price is None:
        return None

    return price * amount