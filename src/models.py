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
    match_level: str = ""
    match_reason: str = ""

    def uid(self) -> str:
        return self.url

    def message(self) -> str:
        classification = self.match_level
        reason = self.match_reason
        classification_block = ""
        if classification:
            classification_block = f"\n{classification}\n{reason}\n"

        return (
            f"📢 {self.source}\n"
            f"{classification_block}\n"
            f"{self.title}\n\n"
            f"{self.url}"
        )
