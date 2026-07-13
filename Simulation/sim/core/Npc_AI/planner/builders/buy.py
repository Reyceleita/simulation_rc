from sim.core.Npc_AI.shopping.shopping_manager import ShoppingManager
from sim.core.Npc_AI.action import Action
from sim.core.Npc_AI.action_types import ActionType

def build(plan, npc, world, block, duration):

    shopping = ShoppingManager().build(npc)

    for item in shopping:
    
        plan.append(
        
            Action(
                ActionType.BUY,
                duration=duration,
                data={
                    "resource": item.resource,
                    "amount": item.amount
                },
                remaining=duration
            )
        )