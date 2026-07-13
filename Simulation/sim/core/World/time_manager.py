"""
time_manager.py

Responsabilidad:
Gestionar el progreso del tiempo dentro de la simulación.

Actualmente:
- Cada tick representa una hora.
- Controla horas, días, meses, años y día de la semana.
- Permite obtener una representación legible de la fecha.

Preparado para futuras ampliaciones:
- Estaciones.
- Festivos.
- Horarios laborales.
- Eventos periódicos.
"""

from dataclasses import dataclass
from sim.core.Npc_AI.schedules.schedule import WeekDay

@dataclass
class GameDate:
    """Representa una fecha dentro del mundo de la simulación."""

    year: int = 1
    month: int = 1
    day: int = 1
    hour: int = 6
    week_day: int = 0  # 0 = Lunes


class TimeManager:
    """Gestiona el progreso del tiempo del mundo."""

    # Días de la semana
    WEEK_DAYS = (
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo",
    )

    # Meses y cantidad de días
    MONTHS = (
        ("Enero", 31),
        ("Febrero", 28),
        ("Marzo", 31),
        ("Abril", 30),
        ("Mayo", 31),
        ("Junio", 30),
        ("Julio", 31),
        ("Agosto", 31),
        ("Septiembre", 30),
        ("Octubre", 31),
        ("Noviembre", 30),
        ("Diciembre", 31),
    )

    def __init__(
        self,
        start_hour: int = 6,
        start_day: int = 1,
        start_month: int = 1,
        start_year: int = 1,
        start_week_day: int = 0,
    ):
        """
        Inicializa el administrador del tiempo.

        Args:
            start_hour: Hora inicial (0-23).
            start_day: Día inicial del mes.
            start_month: Mes inicial (1-12).
            start_year: Año inicial.
            start_week_day:
                Día de la semana.
                0 = Lunes
                1 = Martes
                ...
                6 = Domingo
        """

        self.date = GameDate(
            year=start_year,
            month=start_month,
            day=start_day,
            hour=start_hour,
            week_day=start_week_day,
        )

        # Cantidad total de horas transcurridas desde el inicio
        self.tick = 0

    # ------------------------------------------------------------------
    # Avance del tiempo
    # ------------------------------------------------------------------

    def advance(self) -> None:
        """
        Avanza una hora dentro de la simulación.

        Si se completa un día:
            - Avanza el día del mes.
            - Avanza el día de la semana.

        Si termina el mes:
            - Avanza el mes.

        Si termina el año:
            - Avanza el año.
        """

        self.tick += 1
        self.date.hour += 1

        if self.date.hour < 24:
            return

        # Nuevo día
        self.date.hour = 0
        self.date.day += 1

        # Avanzar día de la semana
        self.date.week_day = (self.date.week_day + 1) % 7

        # Obtener duración del mes actual
        _, days_in_month = self.MONTHS[self.date.month - 1]

        # ¿Terminó el mes?
        if self.date.day <= days_in_month:
            return

        self.date.day = 1
        self.date.month += 1

        # ¿Terminó el año?
        if self.date.month <= 12:
            return

        self.date.month = 1
        self.date.year += 1

    # ------------------------------------------------------------------
    # Información del tiempo
    # ------------------------------------------------------------------

    @property
    def hour(self) -> int:
        return self.date.hour

    @property
    def day(self) -> int:
        return self.date.day

    @property
    def month(self) -> int:
        return self.date.month

    @property
    def year(self) -> int:
        return self.date.year

    @property
    def week_day(self) -> WeekDay:
        return WeekDay(self.date.week_day)

    @property
    def week_day_name(self) -> str:
        """Nombre del día de la semana."""
        return self.WEEK_DAYS[self.date.week_day]

    @property
    def month_name(self) -> str:
        """Nombre del mes actual."""
        return self.MONTHS[self.date.month - 1][0]

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def is_weekend(self) -> bool:
        """Indica si es sábado o domingo."""
        return self.date.week_day >= 5

    def is_workday(self) -> bool:
        """Indica si es un día laboral."""
        return self.date.week_day < 5

    def is_night(self) -> bool:
        """Considera noche desde las 22:00 hasta las 05:59."""
        return self.date.hour >= 22 or self.date.hour < 6

    def is_morning(self) -> bool:
        """Considera mañana desde las 06:00 hasta las 11:59."""
        return 6 <= self.date.hour < 12

    def is_afternoon(self) -> bool:
        """Considera tarde desde las 12:00 hasta las 17:59."""
        return 12 <= self.date.hour < 18

    def is_evening(self) -> bool:
        """Considera tarde-noche desde las 18:00 hasta las 21:59."""
        return 18 <= self.date.hour < 22

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def get_time_string(self) -> str:
        """
        Retorna una representación legible del tiempo actual.

        Ejemplo:
            Lunes, 3 de Enero, Año 1 - 06:00
        """

        return (
            f"{self.week_day_name}, "
            f"{self.day} de {self.month_name}, "
            f"Año {self.year} - "
            f"{self.hour:02d}:00"
        )

    # ------------------------------------------------------------------
    # Reinicio
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reinicia el tiempo al estado inicial."""

        self.date = GameDate()
        self.tick = 0