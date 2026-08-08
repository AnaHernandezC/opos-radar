TECH_KEYWORDS = (
    "INFORMÁTICA",
    "INFORMATICA",
    "SISTEMAS",
    "TECNOLOGÍAS DE LA INFORMACIÓN",
    "TECNOLOGIAS DE LA INFORMACION",
    "TIC",
)
LEVEL_KEYWORDS = ("A1", "A2", "C1")
LOCATION_KEYWORDS = ("VALLADOLID", "PALENCIA", "ZAMORA")


def classify(item):
    text = " ".join(
        part for part in (
            item.title,
            item.organization,
            item.body,
            item.url,
        ) if part
    ).upper()

    tags = []

    if any(keyword in text for keyword in TECH_KEYWORDS):
        tags.append("Informática")

    for level in LEVEL_KEYWORDS:
        if level in text:
            tags.append(level)
            break

    for location in LOCATION_KEYWORDS:
        if location in text:
            tags.append(location.title())
            break

    if "Informática" in tags and any(level in tags for level in LEVEL_KEYWORDS):
        return "🟢 MATCH", " + ".join(tags)

    return "🟡 REVISAR", " + ".join(tags) if tags else "requiere revisión"
