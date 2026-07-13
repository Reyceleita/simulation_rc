from sim.core.resources.resources_types import ResourceCategory

from .shopping_item import ShoppingItem

from .shopping_utils import missing_stock


def build(npc, targets):

    amount = missing_stock(

        npc,

        ResourceCategory.CONSUMER,

        targets[ResourceCategory.CONSUMER]

    )

    if amount <= 0:

        return []

    return [

        ShoppingItem(

            resource=ResourceCategory.CONSUMER,

            amount=amount,

            priority=50

        )

    ]