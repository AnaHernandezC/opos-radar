import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from models import Opportunity

URL = "https://www.adif.es/empleo/oferta-empleo-publico/plazo-solicitud-abierto/-/categories/3460041?p_r_p_categoryId=3460041"

KEYWORDS = [
    "INFORMÁTICA",
    "SISTEMAS",
    "TECNOLOGÍA",
    "TÉCNICO",
    "TÉCNICA",
]


class AdifSource:
    name = "adif"

    def latest(self):
        print("Consultando ADIF...")

        r = requests.get(
            URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        seen = set()

        for link in soup.find_all("a"):
            title = link.get_text(" ", strip=True)
            href = link.get("href", "")
            normalized = title.upper()

            if not title or not href:
                continue
            if not any(keyword in normalized for keyword in KEYWORDS):
                continue

            full_url = urljoin(URL, href)
            if full_url in seen:
                continue

            seen.add(full_url)
            results.append(
                Opportunity(
                    source="ADIF",
                    title=title,
                    url=full_url,
                    organization="ADIF",
                )
            )

        print(f"ADIF: {len(results)} oportunidades coinciden con el filtro")
        return results
