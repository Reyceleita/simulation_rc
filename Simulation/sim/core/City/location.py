from dataclasses import dataclass
from sim.core.City.location_registry import LocationType

@dataclass
class Location:

    id: str

    name: str

    type: LocationType

    position: dict

    capacity: int = 999