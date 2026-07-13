from dataclasses import dataclass
from enum import Enum, auto


class ActivityType(Enum):

    WORK = auto()
    FREE_TIME = auto()
    EAT = auto()
    SLEEP = auto()
    SHOP = auto()
    SOCIALIZE = auto()


class WeekDay(Enum):

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


@dataclass(slots=True)
class RoutineBlock:

    start_hour: int
    end_hour: int
    activity: ActivityType
    priority: int = 0

    @property
    def duration(self):

        if self.end_hour >= self.start_hour:
            return self.end_hour - self.start_hour

        return (24 - self.start_hour) + self.end_hour


class WeeklySchedule:

    def __init__(self):

        self.days = {}

    def get_day(self, week_day):

        return self.days.get(week_day, [])

    def current_block(
        self,
        week_day,
        hour
    ):
        """
        Devuelve el bloque activo para el día y hora indicados.
        """

        blocks = self.days.get(week_day, [])

        for block in blocks:

            # Bloque normal
            if block.start_hour < block.end_hour:

                if block.start_hour <= hour < block.end_hour:
                    return block

            # Bloque que cruza la medianoche
            else:

                if hour >= block.start_hour or hour < block.end_hour:
                    return block

        return None