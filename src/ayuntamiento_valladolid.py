import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://www.valladolid.gob.es/es/tablon-oficial/ayuntamiento-valladolid/empleo-publico"


class AyuntamientoValladolidSource:

    name = "ayuntamiento_valladolid"

    def latest(self):

        r = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        h2 = soup.find("h2")

        if h2:
            title = h2.get_text(" ", strip=True)
        else:
            title = "Empleo Público Valladolid"

        return Opportunity(
            source="Ayuntamiento de Valladolid",
            title=title,
            url=URL,
        )
