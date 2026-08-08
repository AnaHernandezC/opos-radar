import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from models import Opportunity

URL = "https://www.opobusca.com/oposiciones/valladolid"

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

            if not title or len(title) < 8:
                continue

            full_url = urljoin(URL, href)
            if full_url in seen:
                continue

            # OpoBusca is a discovery source: do not apply the restrictive
            # professional/access filter used by official sources.
            if not any(path in full_url for path in ("/ofertas/", "/oposiciones/")):
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

        print(f"OpoBusca: {len(results)} oportunidades detectadas")
        return results
