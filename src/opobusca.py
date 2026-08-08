import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://www.opobusca.com/oposiciones/valladolid"

# Broad discovery filter. Intentionally less restrictive than official-source
# filters so potential A2/labour opportunities are not silently discarded.
KEYWORDS = [
    "TÉCNICO",
    "TÉCNICA",
    "INFORMÁTICA",
    "SISTEMAS",
    "INGENIERO",
    "INGENIERA",
    "GESTIÓN",
    "A2",
    "PERSONAL LABORAL",
    "LABORAL",
]

# Accept individual opportunity pages from the main detail URL families.
DETAIL_URL = re.compile(r"/((?:ofertas|convocatorias)/[^/]+/\d+)(?:$|[?#])")


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
            if full_url in seen:
                continue
            if not DETAIL_URL.search(full_url):
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
