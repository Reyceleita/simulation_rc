"""
main.py
FastAPI para la simulación de ciudades y NPCs.
Expone endpoints para consultar el estado del mundo, ciudades, NPCs,
estadísticas, comercio y avanzar la simulación.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn

# ─────────────────────────────────────────────
# Modelos de respuesta (Pydantic)
# ─────────────────────────────────────────────

class TimeResponse(BaseModel):
    tick: int
    day: int
    hour: int
    time_string: str


class SocialMetricsResponse(BaseModel):
    avg_hunger: float
    avg_money: float
    avg_stress: float
    avg_happiness: float
    wellbeing_index: float


class EmploymentStatsResponse(BaseModel):
    employed: int
    unemployed: int


class CityResourcesResponse(BaseModel):
    food: float


class CityPricesResponse(BaseModel):
    food_price: int


class CityResponse(BaseModel):
    name: str
    type: str
    culture: Dict[str, float]
    base_stress: float
    population: int
    treasury: float
    resources: Dict[str, float]
    prices: Dict[str, int]
    employment: EmploymentStatsResponse
    social_metrics: SocialMetricsResponse

class NPCDecisionsResponse(BaseModel):
    tick: int
    npc_id: int
    chose_action: str
    hunger: float
    energy: float
    happiness: float
    stress: float
    reason: str

class NPCDecisionItemResponse(BaseModel):
    npc_id: int
    chose_action: str
    reason: str
    hunger: float
    energy: float
    happiness: float
    stress: float


class LatestDecisionsResponse(BaseModel):
    tick: int
    total_decisions: int
    decisions: List[
        NPCDecisionItemResponse
    ]

class NPCPersonalityResponse(BaseModel):
    greed: float
    sociability: float
    risk: float
    discipline: float
    empathy: float
    impulsiveness: float


class NPCInventoryResponse(BaseModel):
    food: int
    goods: int


class NPCResponse(BaseModel):
    id: int
    profession: str
    city: str
    money: float
    hunger: float
    energy: float
    happiness: float
    stress: float
    satiety: float
    metabolism: float
    hunger_threshold: int
    personality: NPCPersonalityResponse
    inventory: NPCInventoryResponse
    trade_route: Optional[str]


class NPCMemoryResponse(BaseModel):
    memory_short: Dict[str, float]
    memory_emotional: Dict[str, float]


class NPCRelationshipsResponse(BaseModel):
    npc_id: int
    relationships: Dict[int, float]
    average_relationship: float


class TradeRouteResponse(BaseModel):
    origin: str
    destination: str
    profit: float


class TradeResultResponse(BaseModel):
    success: bool
    amount: int
    price: float
    total_cost: float
    message: str


class GlobalStatsResponse(BaseModel):
    total_npcs: int
    total_money: float
    avg_hunger: float
    avg_happiness: float
    avg_stress: float
    avg_money: float


class WorldHistoryResponse(BaseModel):
    money: List[float]
    hunger: List[float]
    happiness: List[float]
    stress: List[float]


class CityHistoryResponse(BaseModel):
    food: List[float]
    population: List[int]
    employed: List[int]
    unemployed: List[int]
    prices: List[int]
    hunger: List[float]
    money: List[float]
    stress: List[float]
    happiness: List[float]


class TickResponse(BaseModel):
    tick: int
    day: int
    hour: int
    trade_results: List[TradeResultResponse]
    global_stats: GlobalStatsResponse


# ─────────────────────────────────────────────
# Inicialización del mundo (simulación)
# ─────────────────────────────────────────────


try:
    from sim.api.dependences import get_world
    _world = get_world()
except Exception as e:
    print("ERROR IMPORTANDO WORLD:")
    print(e)
    raise e
#except ImportError:
#    _world = None  # Modo demo si no hay módulos de simulación disponibles


# ─────────────────────────────────────────────
# Aplicación FastAPI
# ─────────────────────────────────────────────

app = FastAPI(
    title="City Simulation API",
    description=(
        "API REST para la simulación de ciudades, NPCs, economía y comercio.\n\n"
        "Permite consultar el estado del mundo, avanzar la simulación tick a tick, "
        "y obtener estadísticas detalladas de cada subsistema."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Endpoints: Simulación / Tiempo
# ─────────────────────────────────────────────

@app.get(
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


@app.get(
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


@app.get(
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


@app.get(
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


# ─────────────────────────────────────────────
# Endpoints: Ciudades
# ─────────────────────────────────────────────

@app.get(
    "/cities",
    response_model=List[CityResponse],
    tags=["Ciudades"],
    summary="Listar ciudades",
    description="Retorna todas las ciudades con su estado completo: población, recursos, precios, empleo y métricas sociales.",
)
def list_cities():
    world = get_world()
    result = []
    for city in world.cities:
        social = city.social.calculate(city.npcs)
        employment = city.social.get_employment_stats(city.npcs)
        result.append(_city_to_response(city, social, employment))
    return result


@app.get(
    "/cities/{city_name}",
    response_model=CityResponse,
    tags=["Ciudades"],
    summary="Detalle de ciudad",
    description="Retorna el estado detallado de una ciudad por nombre.",
)
def get_city(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    social = city.social.calculate(city.npcs)
    employment = city.social.get_employment_stats(city.npcs)
    return _city_to_response(city, social, employment)


@app.get(
    "/cities/{city_name}/history",
    response_model=CityHistoryResponse,
    tags=["Ciudades"],
    summary="Historial de ciudad",
    description="Serie temporal de todas las métricas de una ciudad.",
)
def get_city_history(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    h = city.get_history()
    return CityHistoryResponse(
        food=h.get("food", []),
        population=h.get("population", []),
        employed=h.get("employed", []),
        unemployed=h.get("unemployed", []),
        prices=h.get("prices", []),
        hunger=h.get("hunger", []),
        money=h.get("money", []),
        stress=h.get("stress", []),
        happiness=h.get("happiness", []),
    )


@app.get(
    "/cities/{city_name}/history/{metric}",
    response_model=List[float],
    tags=["Ciudades"],
    summary="Historial de métrica específica",
    description=(
        "Retorna la serie temporal de una métrica individual de la ciudad. "
        "Métricas disponibles: food, population, employed, unemployed, prices, "
        "hunger, money, stress, happiness."
    ),
)
def get_city_metric_history(city_name: str, metric: str):
    world = get_world()
    city = _find_city(world, city_name)
    data = city.get_history(metric)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Métrica '{metric}' no encontrada.")
    return data


@app.get(
    "/cities/{city_name}/employment",
    response_model=EmploymentStatsResponse,
    tags=["Ciudades"],
    summary="Estadísticas de empleo",
    description="Cuenta de empleados y desempleados en la ciudad.",
)
def get_city_employment(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    stats = city.get_employment_stats()
    return EmploymentStatsResponse(**stats)


@app.get(
    "/cities/{city_name}/professions",
    response_model=Dict[str, int],
    tags=["Ciudades"],
    summary="Desglose de profesiones",
    description="Cantidad de NPCs por profesión en la ciudad.",
)
def get_city_professions(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.social.get_profession_breakdown(city.npcs)


@app.get(
    "/cities/{city_name}/resources",
    response_model=Dict[str, float],
    tags=["Ciudades"],
    summary="Recursos de la ciudad",
    description="Inventario de recursos (comida, bienes) de la ciudad.",
)
def get_city_resources(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.resources


@app.get(
    "/cities/{city_name}/prices",
    response_model=Dict[str, int],
    tags=["Ciudades"],
    summary="Precios actuales",
    description="Precios de mercado actuales de la ciudad.",
)
def get_city_prices(city_name: str):
    world = get_world()
    city = _find_city(world, city_name)
    return city.cost_of_life


# ─────────────────────────────────────────────
# Endpoints: NPCs
# ─────────────────────────────────────────────

@app.get(
    "/npcs",
    response_model=List[NPCResponse],
    tags=["NPCs"],
    summary="Listar NPCs",
    description="Lista todos los NPCs. Opcionalmente filtra por ciudad o profesión.",
)
def list_npcs(
    city: Optional[str] = Query(None, description="Filtrar por nombre de ciudad"),
    profession: Optional[str] = Query(None, description="Filtrar por profesión"),
    limit: int = Query(50, ge=1, le=500, description="Máximo de NPCs retornados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
):
    world = get_world()
    npcs = world.npcs

    if city:
        npcs = [n for n in npcs if n.city.name.lower() == city.lower()]
    if profession:
        npcs = [n for n in npcs if n.profession.lower() == profession.lower()]

    npcs = npcs[offset: offset + limit]
    return [_npc_to_response(n) for n in npcs]


@app.get(
    "/npcs/{npc_id}",
    response_model=NPCResponse,
    tags=["NPCs"],
    summary="Detalle de NPC",
    description="Retorna el estado completo de un NPC por ID.",
)
def get_npc(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return _npc_to_response(npc)

@app.get(
    "/decisions/latest",
    response_model=
        LatestDecisionsResponse,
    tags=["NPCs"],
    summary=
        "Últimas decisiones globales",
    description=
        "Retorna todas las decisiones "
        "tomadas por los NPCs "
        "durante el último tick.",
)
def get_latest_decisions():
    world = get_world()
    tick = world.time_manager.tick
    decisions = (
        world.decision_tracker
        .get_tick_decisions(tick)
    )
    parsed = [
        NPCDecisionItemResponse(
            npc_id=d.npc_id,
            chose_action=
                d.chosen_action,
            reason=d.reason,
            hunger=d.hunger,
            energy=d.energy,
            happiness=d.happiness,
            stress=d.stress,
        )
        
        for d in decisions
    ]
    return LatestDecisionsResponse(
        tick=tick,
        total_decisions=
            len(parsed),
        decisions=parsed,
    )

@app.get(
    "/npcs/{npc_id}/decisions",
    response_model=NPCDecisionsResponse,
    tags=["NPCs"],
    summary="Desicion del npc",
    description="Retorna la ultima desición tomada por el NPC junto a sus stats",
)
def get_npc_decision(npc_id: int):
    world = get_world()
    response = world.decision_tracker.get_latest(npc_id)
    return NPCDecisionsResponse(
        tick= response.tick,
        chose_action= response.chosen_action,
        energy= response.energy,
        happiness= response.happiness,
        hunger= response.hunger,
        npc_id= response.npc_id,
        reason= response.reason,
        stress= response.stress
    )

@app.get(
    "/npcs/{npc_id}/memory",
    response_model=NPCMemoryResponse,
    tags=["NPCs"],
    summary="Memoria del NPC",
    description="Retorna contadores de memoria a corto plazo y satisfacciones emocionales.",
)
def get_npc_memory(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return NPCMemoryResponse(
        memory_short=dict(npc.memory.memory_short),
        memory_emotional=dict(npc.memory.memory_emotional),
    )


@app.get(
    "/npcs/{npc_id}/relationships",
    response_model=NPCRelationshipsResponse,
    tags=["NPCs"],
    summary="Relaciones sociales del NPC",
    description="Retorna el mapa de relaciones del NPC con otros NPCs (valores en [-1, 1]).",
)
def get_npc_relationships(npc_id: int):
    world = get_world()
    npc = _find_npc(world, npc_id)
    return NPCRelationshipsResponse(
        npc_id=npc_id,
        relationships=dict(npc.social.relationships),
        average_relationship=npc.social.average_relationship(),
    )


@app.get(
    "/npcs/{npc_id}/history",
    response_model=Dict[str, List[float]],
    tags=["NPCs"],
    summary="Historial del NPC",
    description="Serie temporal de estadísticas del NPC (dinero, hambre, felicidad, estrés).",
)
def get_npc_history(npc_id: int):
    world = get_world()
    _find_npc(world, npc_id)  # Valida existencia
    return world.get_npc_history(npc_id)


# ─────────────────────────────────────────────
# Endpoints: Comercio
# ─────────────────────────────────────────────

@app.get(
    "/trade/routes",
    response_model=List[TradeRouteResponse],
    tags=["Comercio"],
    summary="Rutas comerciales activas",
    description="Lista las rutas comerciales vigentes entre ciudades con su rentabilidad.",
)
def get_trade_routes():
    world = get_world()
    routes = world.get_trade_routes()
    return [
        TradeRouteResponse(
            origin=r.origin.name,
            destination=r.destination.name,
            profit=r.profit,
        )
        for r in routes
    ]


@app.get(
    "/trade/classify",
    tags=["Comercio"],
    summary="Clasificar ciudades",
    description="Clasifica las ciudades en compradoras y vendedoras según su ratio comida/población.",
)
def classify_cities():
    world = get_world()
    buyers, sellers = world.trade_manager.classify_cities(world.cities)
    return {
        "buyers": [c.name for c in buyers],
        "sellers": [c.name for c in sellers],
    }


@app.post(
    "/trade/execute",
    response_model=List[TradeResultResponse],
    tags=["Comercio"],
    summary="Ejecutar comercio",
    description="Ejecuta manualmente todas las transacciones comerciales posibles entre ciudades.",
)
def execute_trade():
    world = get_world()
    results = world.trade_manager.trade_between_cities(world.cities)
    return [
        TradeResultResponse(
            success=r.success,
            amount=r.amount,
            price=r.price,
            total_cost=r.total_cost,
            message=r.message,
        )
        for r in results
    ]


# ─────────────────────────────────────────────
# Endpoint raíz
# ─────────────────────────────────────────────

@app.get("/", tags=["Info"])
def root():
    return {
        "name": "City Simulation API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "simulation": ["/simulation/tick", "/simulation/time", "/simulation/stats", "/simulation/history"],
            "cities": ["/cities", "/cities/{name}", "/cities/{name}/history", "/cities/{name}/employment", "/cities/{name}/professions", "/cities/{name}/resources", "/cities/{name}/prices"],
            "npcs": ["/npcs", "/npcs/{id}", "/npcs/{id}/memory", "/npcs/{id}/relationships", "/npcs/{id}/history"],
            "trade": ["/trade/routes", "/trade/classify", "/trade/execute"],
        },
    }


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _find_city(world, name: str):
    for city in world.cities:
        if city.name.lower() == name.lower():
            return city
    raise HTTPException(status_code=404, detail=f"Ciudad '{name}' no encontrada.")


def _find_npc(world, npc_id: int):
    for npc in world.npcs:
        if npc.id == npc_id:
            return npc
    raise HTTPException(status_code=404, detail=f"NPC con id={npc_id} no encontrado.")


def _city_to_response(city, social, employment) -> CityResponse:
    return CityResponse(
        name=city.name,
        type=city.type,
        culture=city.culture,
        base_stress=city.base_stress,
        population=len(city.npcs),
        treasury=city.treasury,
        resources=city.resources,
        prices=city.cost_of_life,
        employment=EmploymentStatsResponse(**employment),
        social_metrics=SocialMetricsResponse(
            avg_hunger=social.avg_hunger,
            avg_money=social.avg_money,
            avg_stress=social.avg_stress,
            avg_happiness=social.avg_happiness,
            wellbeing_index=social.wellbeing_index,
        ),
    )


def _npc_to_response(npc) -> NPCResponse:
    trade_route_str = None
    if npc.trade_route:
        tr = npc.trade_route
        if isinstance(tr, dict):
            trade_route_str = f"{tr.get('from', {}).get('name', '?')} → {tr.get('to', {}).get('name', '?')}"
        else:
            trade_route_str = f"{tr.origin.name} → {tr.destination.name}"

    return NPCResponse(
        id=npc.id,
        profession=npc.profession,
        city=npc.city.name if npc.city else "sin ciudad",
        money=npc.money,
        hunger=npc.hunger,
        energy=npc.energy,
        happiness=npc.happiness,
        stress=npc.stress,
        satiety=npc.satiety,
        metabolism=npc.metabolism,
        hunger_threshold=npc.hunger_threshold,
        personality=NPCPersonalityResponse(**npc.personality),
        inventory=NPCInventoryResponse(**npc.inventory),
        trade_route=trade_route_str,
    )


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)