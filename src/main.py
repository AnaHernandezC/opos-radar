from sources import SOURCES
from notifier import send
from matcher import classify
from state import load, save, get_last, set_last, is_seen, mark_seen


state = load()

for source in SOURCES:

    try:
        items = source.latest()

        if items is None:
            continue

        if not isinstance(items, list):
            items = [items]

        for item in items:
            uid = item.uid()

            # Compatibilidad con el estado antiguo por fuente.
            if get_last(state, source.name) == uid or is_seen(state, uid):
                print(f"{source.name}: sin cambios para {uid}")
                continue

            item.match_level, item.match_reason = classify(item)
            send(item.message())
            mark_seen(state, uid)
            set_last(state, source.name, uid)

    except Exception as e:
        print(f"ERROR en {source.name}: {e}")

save(state)

print("Proceso terminado")
