from typing import List

from sim.snapshots.event_snapshot import EventSnapshot


class EventTracker:

    def __init__(self):
        self.current_tick_events: List[EventSnapshot] = []
        self.history: List[EventSnapshot] = []

    def clear_tick(self):
        self.current_tick_events = []

    def add_event(self, event: EventSnapshot):
        self.current_tick_events.append(event)
        self.history.append(event)

    def get_current_tick_events(self):
        return self.current_tick_events

    def get_history(self):
        return self.history