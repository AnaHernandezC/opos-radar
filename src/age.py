import requests
from bs4 import BeautifulSoup

from models import Opportunity

URL = "https://administracion.gob.es/pagFront/ofertasempleopublico/resultadosEmpleo.htm?referencia=&tipoConvocatoria=2&_ambitoGeografico=1&_comunidadAutonoma=1&_provincia=1&_tipoPlazo=1&_discapacidadGeneral=on&_discapacidadIntelectual=on&_tipoPersonal=1&tipoFechas=intervaloFechas&fechaPublicacionDesde=01%2F08%2F2025&fechaPublicacionHasta=04%2F08%2F2028&tipoPlazaPublicacion=&_tipoBusqueda=on&administracionConvocante=1&_administracionConvocante=1&nivelTitulacion=2&nivelTitulacion=3&_nivelTitulacion=1&orders=id&sort=desc&desde=1&tam=&txtClaveE=inform%C3%A1tica&viaAcceso=2&buscar=true"


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

        print("URL:", r.url)
        print("STATUS:", r.status_code)
        print("CONTENT-TYPE:", r.headers.get("content-type"))
        print("=" * 80)
        print(r.text[:4000])
        print("=" * 80)

        return None
