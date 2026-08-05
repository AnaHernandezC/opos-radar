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

    def uid(self) -> str:
        return self.url

    def message(self) -> str:
        return (
            f"📢 {self.source}\n\n"
            f"{self.title}\n\n"
            f"{self.url}"
        )
