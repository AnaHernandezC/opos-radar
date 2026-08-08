from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://www.opobusca.com/oposiciones/valladolid"

KEYWORDS = [
    "TÉCNICO",
    "TÉCNICA",
    "INFORMÁTICA",
    "SISTEMAS",
    "INGENIERO",
    "INGENIERA",
    "A2",
    "PERSONAL LABORAL",
    "LABORAL",
]

class OpoBuscaSource:
    name = "opobusca"

    def latest(self):
        print("Consultando OpoBusca...")

        r = requests.get(
            URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        seen = set()

        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            href = link["href"]
            normalized = title.upper()

            if not title or len(title) < 8:
                continue
            if not any(keyword in normalized for keyword in KEYWORDS):
                continue

            full_url = urljoin(URL, href)
            if full_url == URL or full_url in seen:
                continue
            if "/oposiciones/" not in full_url and "/convocatorias/" not in full_url and "/ofertas/" not in full_url:
                continue

            seen.add(full_url)
            results.append(
                Opportunity(
                    source="OpoBusca",
                    title=title,
                    url=full_url,
                    organization="OpoBusca",
                )
            )

        print(f"OpoBusca: {len(results)} oportunidades de revisión")
        return results
