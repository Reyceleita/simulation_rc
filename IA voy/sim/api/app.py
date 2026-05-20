from contextlib import asynccontextmanager

from fastapi import FastAPI

from sim.simulation_runner import (
    SimulationRunner,
)

from sim.api.routes.simulation_routes import (
    router as simulation_router,
)
from sim.api.routes.city_routes import (
    router as city_router
)
from sim.api.routes.npc_routes import (
    router as npc_router
)
from sim.api.routes.trade_routes import (
    router as trade_router
)

simulation = SimulationRunner()


@asynccontextmanager
async def lifespan(app: FastAPI):

    simulation.start()

    print("Simulation started")

    yield

    simulation.stop()

    print("Simulation stopped")


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(simulation_router)
app.include_router(city_router)
app.include_router(npc_router)
app.include_router(trade_router)