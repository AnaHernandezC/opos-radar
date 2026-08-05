from models import Opportunity


class AgeSource:

    name = "age"

    def latest(self) -> Opportunity | None:
        return None
