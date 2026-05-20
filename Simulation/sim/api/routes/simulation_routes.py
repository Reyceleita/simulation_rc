from fastapi import APIRouter
from sim.api.models.simulation_models import GlobalStatsResponse, TickResponse, TimeResponse, WorldHistoryResponse
from sim.api.models.trade_models import TradeResultResponse

from sim.api.dependences import (
    get_world,
)
router = APIRouter(
    tags=["Simulation"]
)

@router.get(
    "/simulation/tick",
    response_model=TickResponse,
    tags=["Simulación"],
    summary="Avanzar un tick",
    description="Ejecuta un ciclo completo de la simulación (1 hora de juego) y retorna el estado resultante.",
)
def advance_tick():
    world = get_world()
    world.update()

    trade_routes = world.get_trade_routes()
    trade_results = [
        TradeResultResponse(
            success=True,
            amount=0,
            price=0.0,
            total_cost=0.0,
            message=f"{r.origin.name} → {r.destination.name} (profit {r.profit:.2f})"
        )
        for r in trade_routes
    ]

    global_avg = world.stats_tracker.calculate_global_averages(world.npcs)

    return TickResponse(
        tick=world.time_manager.tick,
        day=world.time_manager.day,
        hour=world.time_manager.hour,
        trade_results=trade_results,
        global_stats=GlobalStatsResponse(
            total_npcs=len(world.npcs),
            total_money=world.population_manager.get_total_money(world.npcs),
            avg_hunger=global_avg.hunger,
            avg_happiness=global_avg.happiness,
            avg_stress=global_avg.stress,
            avg_money=global_avg.money,
        ),
    )


@router.get(
    "/simulation/time",
    response_model=TimeResponse,
    tags=["Simulación"],
    summary="Tiempo actual",
    description="Retorna el tick, día y hora actuales de la simulación.",
)
def get_time():
    world = get_world()
    tm = world.time_manager
    return TimeResponse(
        tick=tm.tick,
        day=tm.day,
        hour=tm.hour,
        time_string=tm.get_time_string(),
    )


@router.get(
    "/simulation/stats",
    response_model=GlobalStatsResponse,
    tags=["Simulación"],
    summary="Estadísticas globales",
    description="Promedios globales de todos los NPCs en el mundo.",
)
def get_global_stats():
    world = get_world()
    avg = world.stats_tracker.calculate_global_averages(world.npcs)
    return GlobalStatsResponse(
        total_npcs=len(world.npcs),
        total_money=world.population_manager.get_total_money(world.npcs),
        avg_hunger=avg.hunger,
        avg_happiness=avg.happiness,
        avg_stress=avg.stress,
        avg_money=avg.money,
    )


@router.get(
    "/simulation/history",
    response_model=WorldHistoryResponse,
    tags=["Simulación"],
    summary="Historial global",
    description="Serie temporal de estadísticas globales (dinero, hambre, felicidad, estrés).",
)
def get_world_history():
    world = get_world()
    history = world.get_stats_history()
    return WorldHistoryResponse(
        money=history.get("money", []),
        hunger=history.get("hunger", []),
        happiness=history.get("happiness", []),
        stress=history.get("stress", []),
    )