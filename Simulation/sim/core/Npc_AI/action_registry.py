from sim.core.Npc_AI.Actions.socialize import socialize
from sim.core.Npc_AI.Actions.economy import buy
from sim.core.Npc_AI.Actions.basics import work, eat, sleep
from sim.core.Npc_AI.action_types import ActionType

from dataclasses import dataclass
from typing import Callable



@dataclass
class ActionHandler:

    start: Callable | None = None

    update: Callable | None = None

    finish: Callable | None = None


ACTION_HANDLERS = {

    ActionType.WORK: ActionHandler(

        start=work.start,

        update=work.update,

        finish=work.finish

    ),
    ActionType.SLEEP: ActionHandler(

        start=sleep.start,

        update=sleep.update,

        finish=sleep.finish

    ),
    ActionType.EAT: ActionHandler(

        start=eat.start,

        update=eat.update,

        finish=eat.finish

    ),
    ActionType.BUY: ActionHandler(

        start=buy.start,

        update=buy.update,

        finish=buy.finish

    ),
    ActionType.SOCIALIZE: ActionHandler(

        start=socialize.start,

        update=socialize.update,

        finish=socialize.finish

    ),
}