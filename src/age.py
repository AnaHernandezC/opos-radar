import re
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://administracion.gob.es/pagFront/ofertasempleopublico/resultadosEmpleo.htm?referencia=&tipoConvocatoria=2&_ambitoGeografico=1&_comunidadAutonoma=1&_provincia=1&_tipoPlazo=1&tipoFechas=intervaloFechas&fechaPublicacionDesde=01%2F08%2F2025&fechaPublicacionHasta=04%2F08%2F2028&_tipoBusqueda=on&administracionConvocante=1&_administracionConvocante=1&nivelTitulacion=2&nivelTitulacion=3&_nivelTitulacion=1&orders=id&sort=desc&desde=1&txtClaveE=inform%C3%A1tica&viaAcceso=2&buscar=true"

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
        detail_errors = 0
        candidates = 0

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

            candidates += 1
            detail_url = urljoin(URL, href)

            try:
                detail = requests.get(
                    detail_url,
                    timeout=30,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                detail.raise_for_status()
            except requests.RequestException as exc:
                detail_errors += 1
                print(f"AGE: no se pudo consultar {detail_url}: {exc}")
                continue

            detail_soup = BeautifulSoup(detail.text, "html.parser")
            text = detail_soup.get_text(" ", strip=True)
            deadline = self._extract_deadline(text)

            if deadline is None:
                print(f"AGE: sin plazo identificable - {title}")
                continue

            if deadline.date() < datetime.now().date():
                print(f"AGE: plazo vencido - {title} ({deadline.date()})")
                continue

            return Opportunity(
                source="AGE",
                title=title,
                url=detail_url,
                deadline=deadline,
                body=text,
                organization="Administración General del Estado",
            )

        if detail_errors and detail_errors >= candidates:
            print("AGE: fuente no disponible; no se puede determinar si hay oportunidades abiertas")
        else:
            print("AGE: ninguna oportunidad abierta coincide con el filtro")

        return None

    @staticmethod
    def _extract_deadline(text):
        match = re.search(
            r"(?:Hasta el|Hasta)\s+(\d{2}/\d{2}/\d{4})",
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return datetime.strptime(match.group(1), "%d/%m/%Y")
