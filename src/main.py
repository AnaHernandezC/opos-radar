from sources import latest
from notifier import send

print("Iniciando...")

item = latest()
print(item)

if item:
    print("Enviando Telegram...")
    send(f"BOCYL\n\n{item[0]}\n{item[1]}")
    print("Enviado")
else:
    print("No hay elementos en el RSS")
