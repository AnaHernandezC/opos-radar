import feedparser

RSS = "https://bocyl.jcyl.es"

def latest():
    feed = feedparser.parse(RSS)

    print("Status:", getattr(feed, "status", ""))
    print("Entries:", len(feed.entries))
    print("Bozo:", feed.bozo)

    if feed.entries:
        e = feed.entries[0]
        return e.title, e.link

    return None
