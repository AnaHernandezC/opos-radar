import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# POC: oportunidades del Ayuntamiento de Valladolid alineadas con el perfil.
VALLADOLID_INCLUDE_KEYWORDS = [
    "INFORMÁTICA",
    "SISTEMAS",
    "TIC",
    "TECNOLOGÍAS",
    "GESTIÓN INFORMÁTICA",
    "TÉCNICO INFORMÁTICO",
    "TÉCNICA INFORMÁTICA",
]

# La Ingeniería Técnica en Informática de Sistemas no se trata como acceso A1.
# Por eso excluimos expresamente puestos de Técnico Superior en este POC.
VALLADOLID_EXCLUDE_KEYWORDS = [
    "TÉCNICO SUPERIOR",
    "POLICÍA",
    "SUBINSPECTOR",
    "PEÓN",
    "PSICÓLOGO",
    "AUXILIAR POLIVALENTE",
]
