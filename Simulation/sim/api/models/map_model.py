from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class CityMarker:

    name: str

    type: str

    population: int

    position: dict



class PositionResponse(BaseModel):

    x: float

    y: float


class LocationResponse(BaseModel):

    id: str

    name: str

    type: str

    position: PositionResponse

class NPCMarkerResponse(BaseModel):

    id: int

    name: str

    profession: str

    location: str

class CityMapResponse(BaseModel):

    city: str
    
    background: str

    locations: list[LocationResponse]

    npcs: list[NPCMarkerResponse]