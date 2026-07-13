from sim.utils.helpers.resources_helpers import get_category_stock


def missing_stock(

    npc,

    category,

    target

):

    current = get_category_stock(

        npc,

        category

    )

    return max(

        target - current,

        0

    )