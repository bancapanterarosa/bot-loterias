import os
import re
import requests
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Configuración desde Render
API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
STRING_SESSION = os.environ.get("TELEGRAM_STRING_SESSION", "")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://tv.panterarosa.store/api/resultados")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

if not STRING_SESSION:
    raise ValueError("❌ No se encontró la variable TELEGRAM_STRING_SESSION")

print("🤖 Bot Extractor Nube - Comercializadora La Pantera Rosa Iniciado...")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

def enviar_a_tv(datos):
    """Envia el resultado parseado al servidor web de la TV"""
    headers = {"Content-Type": "application/json"}
    if WEBHOOK_SECRET:
        headers["x-webhook-secret"] = WEBHOOK_SECRET
    
    try:
        response = requests.post(WEBHOOK_URL, json=datos, headers=headers, timeout=10)
        print(f"📡 Respuesta servidor TV ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error enviando a la TV: {e}")

@client.on(events.NewMessage)
async def procesar_mensaje(event):
    texto = event.raw_text
    if not texto:
        return

    # Mostrar lectura en consola
    print(f"📩 Mensaje recibido: {texto[:60]}...")

    # Detección básica de palabras clave (Lotto Activo, Granjita, etc.)
    texto_lower = texto.lower()
    
    # Si contiene palabras de lotería o un patrón de hora/resultado
    if any(k in texto_lower for k in ["lotto activo", "granjita", "la granjita", "selva plus", "zulia", "tachira"]):
        payload = {
            "texto_raw": texto,
            "origen": "telegram_bot"
        }
        print("🎯 ¡Resultado detectado! Enviando a la TV...")
        enviar_a_tv(payload)

async def main():
    await client.start()
    print("✅ Bot Conectado y Transmitiendo a tv.panterarosa.store...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
