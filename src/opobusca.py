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
    "GESTIÓN",
    "A2",
    "C1",
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

        # OpoBusca renders the Valladolid result list as ordinary links, but
        # the detail URL shape is not stable enough to filter by path. First
        # collect the links belonging to the Valladolid results table.
        table_links = []
        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            href = link["href"]
            if not title or "(Valladolid)" not in title:
                continue
            full_url = urljoin(URL, href)
            if full_url == URL or full_url in seen:
                continue
            if "opobusca.com" not in full_url:
                continue
            table_links.append((title, full_url))
            seen.add(full_url)

        # Inspect the detail page as well as its title. This is important for
        # personal-labour opportunities whose title may simply be "Administrativo"
        # or "Personal de Servicios" while the detail page says "personal laboral".
        for title, full_url in table_links:
            normalized = title.upper()
            relevant = any(keyword in normalized for keyword in KEYWORDS)

            if not relevant:
                try:
                    detail = requests.get(
                        full_url,
                        timeout=10,
                        headers={"User-Agent": "Mozilla/5.0"},
                    )
                    if detail.ok:
                        detail_text = BeautifulSoup(detail.text, "html.parser").get_text(" ", strip=True).upper()
                        relevant = any(keyword in detail_text for keyword in KEYWORDS)
                except requests.RequestException:
                    continue

            if not relevant:
                continue

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
