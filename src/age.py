import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://administracion.gob.es/pag_Home/empleopublico/buscadorEmpleo.html"


class AgeSource:

    name = "age"

    def latest(self):

        r = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        print(soup.title)

        return None
