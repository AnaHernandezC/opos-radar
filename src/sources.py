import feedparser

RSS = "https://www.boe.es/rss.php?c=BOE-S-2-B"


def latest():
    feed = feedparser.parse(RSS)

    print("Status:", getattr(feed, "status", ""))
    print("Entries:", len(feed.entries))
    print("Bozo:", feed.bozo)

    if not feed.entries:
        return None

    entry = feed.entries[0]

    print("Título:", entry.title)

    return (
        entry.title,
        entry.link,
    )
