from models import Opportunity


class BocylSource:

    name = "bocyl"

    def latest(self) -> Opportunity | None:
        # Aquí va el scraping que ya tienes

        # Si no hay resultados:
        # return None

        return Opportunity(
            source="BOCYL",
            title=title,
            url=url,
            published=published,
            body=summary,
            organization="Junta de Castilla y León",
        )
