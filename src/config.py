import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# POC: filtro de oportunidades del Ayuntamiento de Valladolid.
VALLADOLID_INCLUDE_KEYWORDS = [
    "INFORMÁTICA",
    "SISTEMAS",
    "TIC",
    "TECNOLOGÍAS",
    "GESTIÓN INFORMÁTICA",
    "TÉCNICO INFORMÁTICO",
]

VALLADOLID_EXCLUDE_KEYWORDS = [
    "POLICÍA",
    "SUBINSPECTOR",
    "PEÓN",
    "PSICÓLOGO",
    "AUXILIAR POLIVALENTE",
]
