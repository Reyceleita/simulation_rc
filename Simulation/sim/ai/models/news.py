from dataclasses import dataclass
from datetime import datetime


@dataclass
class News:

    id: int
    title: str
    source: str
    created_at: datetime

    def to_dict(self):

        return {

            "id": self.id,

            "title": self.title,

            "source": self.source,

            "created_at": self.created_at.isoformat()

        }