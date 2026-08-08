import re
from datetime import date, datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Opportunity
from config import (
    VALLADOLID_INCLUDE_KEYWORDS,
    VALLADOLID_EXCLUDE_KEYWORDS,
)


URL = "https://www.valladolid.gob.es/es/tablon-oficial/ayuntamiento-valladolid/empleo-publico"

MONTHS = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12,
}


def _extract_deadline(text):
    normalized = " ".join(text.upper().split())

    # Ejemplos: HASTA EL 13/04/2026 o HASTA EL 13-04-2026
    numeric = re.findall(
        r"HASTA\s+(?:EL\s+)?(\d{1,2})[/-](\d{1,2})[/-](\d{4})",
        normalized,
    )
    if numeric:
        day, month, year = map(int, numeric[-1])
        return date(year, month, day)

    # Ejemplos: HASTA EL 13 DE ABRIL DE 2026
    named = re.findall(
        r"HASTA\s+(?:EL\s+)?(\d{1,2})\s+DE\s+([A-ZÁÉÍÓÚ]+)\s+DE\s+(\d{4})",
        normalized,
    )
    if named:
        day, month_name, year = named[-1]
        month = MONTHS.get(month_name)
        if month:
            return date(int(year), month, int(day))

    return None


def _context_text(link):
    current = link

    for _ in range(6):
        current = current.parent
        if current is None:
            break

        text = current.get_text(" ", strip=True)

        if "Fecha de publicación:" in text and len(text) < 5000:
            return text

    return link.get_text(" ", strip=True)


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
        today = date.today()

        for link in soup.find_all("a"):
            title = link.get_text(" ", strip=True)
            normalized = title.upper()

            if not title:
                continue

            if any(keyword in normalized for keyword in VALLADOLID_EXCLUDE_KEYWORDS):
                continue

            if not any(keyword in normalized for keyword in VALLADOLID_INCLUDE_KEYWORDS):
                continue

            context = _context_text(link)
            deadline = _extract_deadline(context)

            # Para este POC solo avisamos de oportunidades realmente accionables.
            # Si no podemos identificar un plazo, preferimos no generar un falso positivo.
            if deadline is None or deadline < today:
                continue

            href = link.get("href", "")
            if not href:
                continue

            return Opportunity(
                source="Ayuntamiento de Valladolid",
                title=title,
                url=urljoin(URL, href),
                deadline=datetime.combine(deadline, datetime.min.time()),
                body=context,
                organization="Ayuntamiento de Valladolid",
            )

        print("Valladolid: ninguna oportunidad abierta coincide con el filtro")
        return None
