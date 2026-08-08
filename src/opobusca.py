import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://www.opobusca.com/oposiciones/valladolid"

INCLUDE_KEYWORDS = [
    "TÉCNICO", "TÉCNICA", "INFORMÁTICA", "SISTEMAS",
    "INGENIERO", "INGENIERA", "GESTIÓN", "ADMINISTRATIVO",
    "ADMINISTRATIVA", "A2", "C1", "PERSONAL LABORAL", "LABORAL",
]

EXCLUDE_KEYWORDS = [
    "POLICÍA", "POLICIA", "BOMBERO", "BOMBEROS", "PERSONAL DE OFICIOS",
    "PERSONAL SERVICIOS", "TRABAJO SOCIAL", "ENFERMER", "CELADOR",
]

DETAIL_URL = re.compile(r"/(?:ofertas|convocatorias)/[^/]+/[^/]+/\d+(?:$|[?#])")

class OpoBuscaSource:
    name = "opobusca"

    def latest(self):
        print("Consultando OpoBusca...")
        r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        results, seen = [], set()
        cutoff = datetime.now() - timedelta(days=45)

        for link in soup.find_all("a", href=True):
            title = link.get_text(" ", strip=True)
            normalized = title.upper()
            full_url = urljoin(URL, link["href"])

            if not title or len(title) < 8 or full_url in seen:
                continue
            if not DETAIL_URL.search(full_url):
                continue
            if any(k in normalized for k in EXCLUDE_KEYWORDS):
                continue
            if not any(k in normalized for k in INCLUDE_KEYWORDS):
                continue

            seen.add(full_url)
            results.append(Opportunity(source="OpoBusca", title=title, url=full_url, organization="OpoBusca"))

        print(f"OpoBusca: {len(results)} oportunidades de revisión")
        return results
