import requests
from bs4 import BeautifulSoup

URL = "https://www.valladolid.gob.es/es/tablon-oficial/ayuntamiento-valladolid/empleo-publico"


def latest():
    r = requests.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    title = None
    link = URL

    h2 = soup.find("h2")
    if h2:
        title = h2.get_text(" ", strip=True)

    if not title:
        title = "Empleo Público Valladolid"

    return title, link
