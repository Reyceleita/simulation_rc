"""
time_manager.py
Responsabilidad: Gestión del tiempo y ciclo día/noche.
"""

class TimeManager:
    """Gestiona el progreso del tiempo en el mundo."""

    def __init__(self, start_hour: int = 6, start_day: int = 1):
        self.hour = start_hour
        self.day = start_day
        self.tick = 0

    def advance(self) -> None:
        """Avanza una hora en el tiempo."""
        self.tick += 1
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1

    def get_time_string(self) -> str:
        """Retorna representación legible del tiempo actual."""
        return f"Día {self.day} Hora {self.hour}"

    def reset(self) -> None:
        """Reinicia el tiempo a los valores iniciales."""
        self.hour = 6
        self.day = 1
        self.tick = 0
