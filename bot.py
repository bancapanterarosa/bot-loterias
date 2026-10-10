import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Obtener variables desde Render
API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
STRING_SESSION = os.environ.get("TELEGRAM_STRING_SESSION", "")

if not STRING_SESSION:
    raise ValueError("❌ No se encontró la variable TELEGRAM_STRING_SESSION en Render.")

print("🤖 Iniciando Bot Extractor Nube - Comercializadora La Pantera Rosa...")

# Inicializar cliente usando la sesión generada
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage)
async def my_event_handler(event):
    # Aquí procesas los mensajes entrantes de los canales
    print(f"📩 Mensaje recibido: {event.raw_text}")

async def main():
    await client.start()
    print("✅ Bot Conectado y Escuchando Canales en Vivo...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
