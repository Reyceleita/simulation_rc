from sim.core.resources.resources_types import ResourceCategory

from .shopping_item import ShoppingItem

from .shopping_utils import missing_stock


def build(npc, targets):

    if npc.money < 200:

        return []

    amount = missing_stock(

        npc,

        ResourceCategory.LUXURY,

        targets[ResourceCategory.LUXURY]

    )

    if amount <= 0:

        return []

    return [

        ShoppingItem(

            resource=ResourceCategory.LUXURY,

            amount=amount,

            priority=10

        )

    ]