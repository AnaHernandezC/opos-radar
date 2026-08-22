from sources import SOURCES
from notifier import send
from matcher import classify
from state import load, save, get_last, set_last, is_seen, mark_seen

MATCHER_VERSION = "2026-08-22-v5"

state = load()
reevaluate = state.get("_matcher_version") != MATCHER_VERSION

for source in SOURCES:

    try:
        items = source.latest()

        if items is None:
            continue

        if not isinstance(items, list):
            items = [items]

        for item in items:
            uid = item.uid()

            # Cuando cambia el matcher, reevaluamos una vez los elementos
            # ya conocidos para que reciban la nueva clasificación.
            if not reevaluate and (get_last(state, source.name) == uid or is_seen(state, uid)):
                print(f"{source.name}: sin cambios para {uid}")
                continue

            item.match_level, item.match_reason = classify(item)
            send(item.message())
            mark_seen(state, uid)
            set_last(state, source.name, uid)

    except Exception as e:
        print(f"ERROR en {source.name}: {e}")

state["_matcher_version"] = MATCHER_VERSION
save(state)

print("Proceso terminado")
