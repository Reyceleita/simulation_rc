from .schedule import *


class WorkerSchedule(WeeklySchedule):

    def __init__(self):

        super().__init__()

        work_day = [

            RoutineBlock(6, 7, ActivityType.EAT),

            RoutineBlock(8, 16, ActivityType.WORK, priority=100),

            RoutineBlock(16, 18, ActivityType.SOCIALIZE),

            RoutineBlock(18, 19, ActivityType.EAT),

            RoutineBlock(19, 22, ActivityType.FREE_TIME),

            RoutineBlock(22, 6, ActivityType.SLEEP),


        ]

        saturday = [

            RoutineBlock(8, 9, ActivityType.EAT),

            RoutineBlock(10, 12, ActivityType.SHOP),

            RoutineBlock(12, 13, ActivityType.EAT),

            RoutineBlock(13, 15, ActivityType.SOCIALIZE),
            
            RoutineBlock(15, 22, ActivityType.FREE_TIME),

            RoutineBlock(22, 8, ActivityType.SLEEP),


        ]

        sunday = [

            RoutineBlock(8, 9, ActivityType.EAT),

            RoutineBlock(10, 18, ActivityType.SOCIALIZE),

            RoutineBlock(18, 19, ActivityType.EAT),

            RoutineBlock(19, 22, ActivityType.FREE_TIME),

            RoutineBlock(22, 8, ActivityType.SLEEP),


        ]

        self.days = {

            WeekDay.MONDAY: work_day,

            WeekDay.TUESDAY: work_day,

            WeekDay.WEDNESDAY: work_day,

            WeekDay.THURSDAY: work_day,

            WeekDay.FRIDAY: work_day,

            WeekDay.SATURDAY: saturday,

            WeekDay.SUNDAY: sunday,

        }