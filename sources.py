import feedparser
RSS="https://bocyl.jcyl.es/boletines/rss.xml"
def latest():
    f=feedparser.parse(RSS)
    if not f.entries: return None
    e=f.entries[0]
    return e.title,e.link
