import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from models import Opportunity

URL = "https://administracion.gob.es/pagFront/ofertasempleopublico/resultadosEmpleo.htm?referencia=&tipoConvocatoria=2&_ambitoGeografico=1&_comunidadAutonoma=1&_provincia=1&_tipoPlazo=1&_discapacidadGeneral=on&_discapacidadIntelectual=on&_tipoPersonal=1&tipoFechas=intervaloFechas&fechaPublicacionDesde=01%2F08%2F2025&fechaPublicacionHasta=04%2F08%2F2028&tipoPlazaPublicacion=&_tipoBusqueda=on&administracionConvocante=1&_administracionConvocante=1&nivelTitulacion=2&nivelTitulacion=3&_nivelTitulacion=1&orders=id&sort=desc&desde=1&tam=&txtClaveE=inform%C3%A1tica&viaAcceso=2&buscar=true"

KEYWORDS = [
    "GESTIÓN DE SISTEMAS E INFORMÁTICA",
    "TÉCNICOS AUXILIARES DE INFORMÁTICA",
]

EXCLUDE_KEYWORDS = [
    "TÉCNICO SUPERIOR",
]


class AgeSource:

    name = "age"

    def latest(self):
        print("Consultando AGE...")

        r = requests.get(
            URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        seen_urls = set()

        for link in soup.find_all("a"):
            href = link.get("href", "")
            title = link.get_text(" ", strip=True)
            normalized = title.upper()

            if not title or not href:
                continue

            if any(keyword in normalized for keyword in EXCLUDE_KEYWORDS):
                continue

            if not any(keyword in normalized for keyword in KEYWORDS):
                continue

            full_url = urljoin(URL, href)
            if full_url in seen_urls:
                continue

            seen_urls.add(full_url)
            results.append(
                Opportunity(
                    source="AGE",
                    title=title,
                    url=full_url,
                    organization="Administración General del Estado",
                )
            )

        print(f"AGE: {len(results)} oportunidades coinciden con el filtro")
        return results
