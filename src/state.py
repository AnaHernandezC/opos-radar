import json
from pathlib import Path

STATE_FILE = Path("data/state.json")


def load():
    if not STATE_FILE.exists():
        return {}

    return json.loads(
        STATE_FILE.read_text(encoding="utf-8")
    )


def save(state):
    STATE_FILE.parent.mkdir(exist_ok=True)

    STATE_FILE.write_text(
        json.dumps(
            state,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def get_last(state, source):
    return state.get(source)


def set_last(state, source, value):
    state[source] = value


def is_seen(state, uid):
    seen = state.get("seen", {})
    return uid in seen


def mark_seen(state, uid):
    state.setdefault("seen", {})[uid] = True
