from .builders import buy
from .builders import work
from .builders import eat
from .builders import sleep

from ..schedules.schedule import ActivityType

PLANNER_BUILDERS = {

    ActivityType.WORK: work,

    ActivityType.EAT: eat,

    ActivityType.SLEEP: sleep,
    
    ActivityType.SHOP: buy,

}