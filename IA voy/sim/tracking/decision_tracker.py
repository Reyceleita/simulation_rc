from collections import defaultdict, deque

from sim.snapshots.decision_snapshot import (
    DecisionSnapshot,
)


class DecisionTracker:

    def __init__(self, max_history=500):

        self.max_history = max_history

        # Historial individual
        self.npc_history = defaultdict(
            lambda: deque(maxlen=max_history)
        )

        # Historial global por tick
        self.tick_history = defaultdict(list)

    def record(
        self,
        snapshot: DecisionSnapshot,
    ):

        # NPC history
        self.npc_history[
            snapshot.npc_id
        ].append(snapshot)

        # Tick history
        self.tick_history[
            snapshot.tick
        ].append(snapshot)

    def get_npc_history(
        self,
        npc_id: int,
    ):

        return list(
            self.npc_history.get(
                npc_id,
                [],
            )
        )

    def get_latest(
        self,
        npc_id: int,
    ):

        history = self.npc_history.get(
            npc_id,
            [],
        )

        return (
            history[-1]
            if history
            else None
        )

    def get_tick_decisions(
        self,
        tick: int,
    ):

        return self.tick_history.get(
            tick,
            [],
        )