from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EventSnapshot:
    tick: int
    type: str
    data: Dict[str, Any]