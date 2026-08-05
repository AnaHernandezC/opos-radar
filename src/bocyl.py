from models import Opportunity

return [
    Opportunity(
        source="BOCYL",
        title=title,
        url=url,
        published=published,
        body=summary,
        organization="Junta de Castilla y León",
    )
]
