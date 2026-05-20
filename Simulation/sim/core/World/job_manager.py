"""
job_manager.py
Responsabilidad: Asignación y gestión de empleos/profesiones.
"""

import random
from typing import Dict, List, Any


class JobManager:
    """
    Responsable de:
    - Distribuir profesiones según configuración de ciudad
    - Manejar desempleo y ajustes por redondeo
    """

    def __init__(self, professions_registry: Dict[str, Any]):
        self.professions = professions_registry

    def assign_jobs(self, city: Any) -> None:
        """
        Asigna profesiones a NPCs de una ciudad según distribución configurada.

        Args:
            city: Objeto City con atributos npcs y jobs_distribution
        """
        npcs = city.npcs
        total = len(npcs)

        if total == 0:
            return

        distribution = city.jobs_distribution

        # Calcular conteos por profesión
        job_counts = {
            job: int(total * ratio)
            for job, ratio in distribution.items()
        }

        # Ajuste por redondeo - asignar excedentes a desempleados
        while sum(job_counts.values()) < total:
            job_counts["unemployed"] = job_counts.get("unemployed", 0) + 1

        # Mezclar NPCs para asignación aleatoria
        random.shuffle(npcs)

        # Asignar profesiones
        index = 0
        for job, count in job_counts.items():
            for _ in range(count):
                if index >= total:
                    break
                npc = npcs[index]
                npc.profession = job
                npc.job = self.professions.get(job)
                index += 1

    def get_profession_counts(self, city: Any) -> Dict[str, int]:
        """Retorna conteo de profesiones en una ciudad."""
        counts = {}
        for npc in city.npcs:
            prof = getattr(npc, 'profession', 'unknown')
            counts[prof] = counts.get(prof, 0) + 1
        return counts

    def count_unemployed(self, city: Any) -> int:
        """Cuenta NPCs desempleados en una ciudad."""
        return sum(1 for n in city.npcs if getattr(n, 'profession', None) == "unemployed")

    def count_workers(self, city: Any) -> int:
        """Cuenta trabajadores activos en una ciudad."""
        return sum(1 for n in city.npcs if getattr(n, 'profession', None) == "worker")
