from sources import latest
from notifier import send
from state import load, save

item = latest()

if not item:
    raise SystemExit()

title, url = item

state = load()

if state.get("last_url") == url:
    print("Sin cambios")
    raise SystemExit()

send(f"{title}\n\n{url}")

state["last_url"] = url
save(state)

print("Notificación enviada")
