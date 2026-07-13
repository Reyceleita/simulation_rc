"""
Genera toda la lista de compras del NPC.
"""

from .inventory_targets import get_targets

from . import food

from . import consumer_goods

from . import luxury


class ShoppingManager:

    def build(self, npc):

        targets = get_targets(npc)

        shopping = []

        shopping.extend(

            food.build(

                npc,

                targets

            )

        )

        shopping.extend(

            consumer_goods.build(

                npc,

                targets

            )

        )

        shopping.extend(

            luxury.build(

                npc,

                targets

            )

        )

        shopping.sort(

            key=lambda x: x.priority,

            reverse=True

        )

        return shopping