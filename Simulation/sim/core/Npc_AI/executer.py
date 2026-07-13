from sim.core.Npc_AI.action_registry import ACTION_HANDLERS


def update(npc, world):

    # Si no hay acción actual,
    # intentar comenzar otra.

    if npc.current_action is None:

        _start_next_action(npc)

        if npc.current_action is None:
            return

    action = npc.current_action

    handler = ACTION_HANDLERS[action.type]

    # Primer tick

    if action.elapsed == 0:

        if handler.start:

            handler.start(
                action,
                npc,
                world
            )

    # Tick de ejecución

    if handler.update:

        handler.update(
            action,
            npc,
            world
        )

    action.elapsed += 1
    action.remaining -= 1

    # ¿Terminó?

    if action.remaining <= 0:

        if handler.finish:

            handler.finish(
                action,
                npc,
                world
            )

        npc.current_action = None

def _start_next_action(npc):

    if not npc.daily_plan:
        return

    npc.current_action = npc.daily_plan.popleft()

