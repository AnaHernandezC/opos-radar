from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Opportunity:
    source: str
    title: str
    url: str

    published: datetime | None = None
    deadline: datetime | None = None

    body: str = ""
    organization: str = ""
    location: str = ""

    def uid(self) -> str:
        """
        Identificador único estable.
        """
        return self.url
