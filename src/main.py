from sources import SOURCES
from notifier import send
from state import load, save, get_last, set_last


state = load()

for source in SOURCES:

    item = source.latest()

    if not item:
        continue

    uid = item.uid()

    if get_last(state, source.name) == uid:
        print(f"{source.name}: sin cambios")
        continue

    send(item.message())

    set_last(state, source.name, uid)

save(state)

print("Proceso terminado")
