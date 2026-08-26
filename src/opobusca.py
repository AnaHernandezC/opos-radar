import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity

URLS = (
    "https://www.opobusca.com/oposiciones/valladolid",
    "https://www.opobusca.com/oposiciones/zamora",
    "https://www.opobusca.com/oposiciones/palencia",
)

# OpoBusca is broad. The radar is not intended to surface generic
# administration, employment, or technical posts that are unrelated to IT.
INCLUDE_KEYWORDS = [
    "INFORMÁTICA", "INFORMATICA", "INFORMÁTICO", "INFORMATICO",
    "SISTEMAS", "TIC", "TECNOLOGÍAS DE LA INFORMACIÓN",
    "TECNOLOGIAS DE LA INFORMACION", "INGENIERÍA INFORMÁTICA",
    "INGENIERIA INFORMATICA", "INGENIERO INFORMÁTICO", "INGENIERO INFORMATICO",
    "TÉCNICO DE INFORMÁTICA", "TECNICO DE INFORMATICA",
    "TÉCNICO AUXILIAR DE INFORMÁTICA", "TECNICO AUXILIAR DE INFORMATICA",
    "GESTIÓN INFORMÁTICA", "GESTION INFORMATICA",
    "TRANSFORMACIÓN DIGITAL", "TRANSFORMACION DIGITAL",
    "ADMINISTRACIÓN ELECTRÓNICA", "ADMINISTRACION ELECTRONICA",
]

EXCLUDE_KEYWORDS = [
    "POLICÍA", "POLICIA", "BOMBERO", "BOMBEROS", "PERSONAL DE OFICIOS",
    "PERSONAL SERVICIOS", "TRABAJO SOCIAL", "ENFERMER", "CELADOR",
    "AUXILIAR ADMINISTRATIVO", "AUXILIAR ADMINISTRATIVA",
]

DETAIL_URL = re.compile(r"/(?:ofertas|convocatorias)/[^/]+/[^/]+/\d+(?:$|[?#])")
DATE_RE = re.compile(r"(\d{2}/\d{2}/\d{4})")

class OpoBuscaSource:
    name = "opobusca"

    def latest(self):
        print("Consultando OpoBusca...")
        cutoff = datetime.now() - timedelta(days=45)
        results, seen = [], set()

        for page_url in URLS:
            r = requests.get(page_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all("a", href=True):
                title = link.get_text(" ", strip=True)
                normalized = title.upper()
                full_url = urljoin(page_url, link["href"])

                if not title or len(title) < 8 or full_url in seen:
                    continue
                if not DETAIL_URL.search(full_url):
                    continue
                if any(k in normalized for k in EXCLUDE_KEYWORDS):
                    continue
                if not any(k in normalized for k in INCLUDE_KEYWORDS):
                    continue

                date_match = DATE_RE.search(title)
                if date_match:
                    published = datetime.strptime(date_match.group(1), "%d/%m/%Y")
                    if published < cutoff:
                        continue
                else:
                    published = None

                seen.add(full_url)
                results.append(
                    Opportunity(
                        source="OpoBusca",
                        title=title,
                        url=full_url,
                        organization="OpoBusca",
                        published=published,
                    )
                )

        print(f"OpoBusca: {len(results)} oportunidades de revisión")
        return results
