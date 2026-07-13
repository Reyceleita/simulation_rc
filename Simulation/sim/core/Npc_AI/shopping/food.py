from sim.core.resources.resources_types import ResourceCategory

from .shopping_item import ShoppingItem

from .shopping_utils import missing_stock


def build(npc, targets):

    amount = missing_stock(

        npc,

        ResourceCategory.FOOD,

        targets[ResourceCategory.FOOD]

    )

    if amount <= 0:

        return []

    return [

        ShoppingItem(

            resource=ResourceCategory.FOOD,

            amount=amount,

            priority=100

        )

    ]