from collections import deque

from .planner_registry import PLANNER_BUILDERS


class Planner:

    def build(self, npc, world):

        plan = deque()

        hour = world.time_manager.hour
        day = world.time_manager.week_day

        routine = npc.schedule.get_day(day)

        for block in routine:

            remaining = self._remaining_hours(block, hour)

            if remaining <= 0:
                continue

            builder = PLANNER_BUILDERS.get(block.activity)

            if builder is None:
                continue

            builder.build(
                plan=plan,
                npc=npc,
                world=world,
                block=block,
                duration=remaining
            )

        return plan

    def _remaining_hours(self, block, current_hour):

        # -----------------------
        # Bloque normal
        # -----------------------

        if block.start_hour < block.end_hour:

            if current_hour < block.start_hour:

                return block.end_hour - block.start_hour

            if current_hour >= block.end_hour:

                return 0

            return block.end_hour - current_hour

        # -----------------------
        # Cruza medianoche
        # -----------------------

        if current_hour >= block.start_hour:

            return (24 - current_hour) + block.end_hour

        if current_hour < block.end_hour:

            return block.end_hour - current_hour

        return 0