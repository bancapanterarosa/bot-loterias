import os
import re
import asyncio
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("TELEGRAM_API_ID", "39020348"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "c3a9b5069c19c929e2dcd2d4899fadfa")
SESSION_STRING = os.environ.get("TELEGRAM_STRING_SESSION", "")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://tv.panterarosa.store/api/webhook/resultado")
SECRET_KEY = os.environ.get("WEBHOOK_SECRET", "pantera_secret_2026")

MAPA_LOTERIAS = {
    'lotto activo': 'lottoActivo',
    'la granjita': 'laGranjita',
    'selva plus': 'selvaPlus',
    'guacharo activo': 'guacharoActivo',
    'guacharito': 'guacharito',
    'granja millonaria': 'granjaMillonaria',
    'granjazo': 'granjazo',
    'monje millonario': 'monjeMillonario',
    'ruleta activa': 'ruletaActiva',
    'la ricachona': 'laRicachona'
}

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage)
async def manejar_mensaje(event):
    texto = event.message.text or ""
    texto_lower = texto.lower()
    
    hora_match = re.search(r'(\d{1,2}:\d{2}\s?[ap]\.?m\.?)', texto, re.IGNORECASE)
    num_match = re.search(r'\b(\d{1,2})\b', texto)
    
    if hora_match and num_match:
        hora = hora_match.group(1).upper().replace('.', '').strip()
        numero = num_match.group(1).zfill(2)
        
        loteria_detectada = None
        for clave, valor in MAPA_LOTERIAS.items():
            if clave in texto_lower:
                loteria_detectada = valor
                break
        
        if loteria_detectada:
            payload = {
                "loteria": loteria_detectada,
                "hora": hora,
                "numero": numero,
                "secret": SECRET_KEY
            }
            try:
                res = requests.post(WEBHOOK_URL, json=payload, timeout=5)
                print(f"🚀 [TV ACTUALIZADA] {loteria_detectada} -> {hora} | Número: {numero} | HTTP {res.status_code}")
            except Exception as e:
                print(f"❌ [ERROR WEBHOOK] {e}")

async def main():
    print("🤖 Bot Extractor Nube - Comercializadora La Pantera Rosa")
    await client.start()
    print("✅ Bot Conectado y Escuchando Canales en Vivo...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
