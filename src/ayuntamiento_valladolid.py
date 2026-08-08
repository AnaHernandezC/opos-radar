import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from models import Opportunity
from config import (
    VALLADOLID_INCLUDE_KEYWORDS,
    VALLADOLID_EXCLUDE_KEYWORDS,
)


URL = "https://www.valladolid.gob.es/es/tablon-oficial/ayuntamiento-valladolid/empleo-publico"


class AyuntamientoValladolidSource:

    name = "ayuntamiento_valladolid"

    def latest(self):
        print("Consultando Ayuntamiento de Valladolid...")

        r = requests.get(
            URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find_all("a"):
            title = link.get_text(" ", strip=True)
            normalized = title.upper()

            if not title:
                continue

            if any(keyword in normalized for keyword in VALLADOLID_EXCLUDE_KEYWORDS):
                continue

            if not any(keyword in normalized for keyword in VALLADOLID_INCLUDE_KEYWORDS):
                continue

            href = link.get("href", "")
            if not href:
                continue

            return Opportunity(
                source="Ayuntamiento de Valladolid",
                title=title,
                url=urljoin(URL, href),
                organization="Ayuntamiento de Valladolid",
            )

        print("Valladolid: ninguna oportunidad coincide con el filtro")
        return None
