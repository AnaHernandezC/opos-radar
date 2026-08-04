from sources import latest
from notifier import send
t=latest()
if t:
    send(f"BOCYL\n\n{t[0]}\n{t[1]}")
