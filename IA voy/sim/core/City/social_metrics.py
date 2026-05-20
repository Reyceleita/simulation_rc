"""
social_metrics.py
Responsabilidad: Cálculo de métricas sociales y bienestar.
"""

from typing import List, Any, Dict
from dataclasses import dataclass


@dataclass
class SocialMetrics:
    """Métricas sociales agregadas de una población."""
    avg_hunger: float
    avg_money: float
    avg_stress: float
    avg_happiness: float

    @property
    def wellbeing_index(self) -> float:
        """Índice compuesto de bienestar (0-100)."""
        if not all([self.avg_happiness, self.avg_stress is not None]):
            return 0.0
        # Menos hambre + menos estrés + más felicidad = mejor bienestar
        return max(0, min(100, 
            (1 - self.avg_hunger) * 30 +
            (1 - self.avg_stress) * 30 +
            self.avg_happiness * 40
        ))


class SocialMetricsCalculator:
    """
    Responsable de:
    - Calcular métricas sociales agregadas (hambre, estrés, felicidad)
    - Calcular estadísticas de empleo
    """

    def calculate(self, npcs: List[Any]) -> SocialMetrics:
        """
        Calcula métricas sociales promedio de una población.

        Args:
            npcs: Lista de NPCs

        Returns:
            Métricas sociales calculadas
        """
        if not npcs:
            return SocialMetrics(0, 0, 0, 0)

        total = len(npcs)

        return SocialMetrics(
            avg_hunger=sum(n.hunger for n in npcs) / total,
            avg_money=sum(n.money for n in npcs) / total,
            avg_stress=sum(n.stress for n in npcs) / total,
            avg_happiness=sum(n.happiness for n in npcs) / total
        )

    def get_employment_stats(self, npcs: List[Any]) -> Dict[str, int]:
        """
        Calcula estadísticas de empleo.

        Returns:
            Dict con 'employed' y 'unemployed'
        """
        employed = sum(1 for n in npcs if getattr(n, 'profession', 'unemployed') != 'unemployed')
        unemployed = len(npcs) - employed

        return {
            "employed": employed,
            "unemployed": unemployed
        }

    def get_profession_breakdown(self, npcs: List[Any]) -> Dict[str, int]:
        """
        Desglose de profesiones.

        Returns:
            Dict {profesión: cantidad}
        """
        breakdown = {}
        for npc in npcs:
            prof = getattr(npc, 'profession', 'unknown')
            breakdown[prof] = breakdown.get(prof, 0) + 1
        return breakdown
