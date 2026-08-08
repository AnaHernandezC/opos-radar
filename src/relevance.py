from models import Opportunity

CLASSIFICATION_VERSION = "2026-08-08-v1"

TECH_KEYWORDS = (
    "INFORMÁTICA",
    "INFORMATICA",
    "SISTEMAS",
    "TECNOLOGÍA",
    "TECNOLOGIA",
    "TIC",
    "INGENIERO TÉCNICO",
    "INGENIERA TÉCNICA",
    "INGENIERO EN INFORMÁTICA",
    "INGENIERA EN INFORMÁTICA",
)
LEVEL_KEYWORDS = ("A2", "C1", "GRUPO A2", "GRUPO C1")
ADMIN_KEYWORDS = ("ADMINISTRATIVO", "ADMINISTRATIVA", "GESTIÓN", "GESTION")
PREFERRED_LOCATIONS = ("VALLADOLID", "PALENCIA", "ZAMORA")


def classify(item: Opportunity) -> tuple[str, list[str]]:
    text = " ".join((item.title, item.body, item.organization, item.url)).upper()

    is_tech = any(keyword in text for keyword in TECH_KEYWORDS)
    level = next((keyword for keyword in LEVEL_KEYWORDS if keyword in text), None)
    location = next((place for place in PREFERRED_LOCATIONS if place in text), None)
    is_admin = any(keyword in text for keyword in ADMIN_KEYWORDS)

    if is_tech and level and location:
        return "🟢 MATCH", [level, "Informática", location.title()]

    if is_tech and level:
        return "🟢 MATCH", [level, "Informática"]

    if is_tech:
        return "🟡 REVISAR", ["Informática"]

    if level and (is_admin or "TÉCNICO" in text or "TECNICA" in text):
        return "🟡 REVISAR", [level]

    if is_admin:
        return "🟡 REVISAR", ["Administrativo"]

    return "🟡 REVISAR", []


def format_message(item: Opportunity) -> str:
    status, tags = classify(item)
    tag_line = " + ".join(tags)

    return (
        f"📢 {item.source}\n\n"
        f"{status}\n"
        f"{tag_line}\n\n"
        f"{item.title}\n\n"
        f"{item.url}"
    )
