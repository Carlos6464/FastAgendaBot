# Em app/routers/telegram_webhook.py
import httpx
from fastapi import APIRouter, Request
from app.services import bot_service
from app.schemas import BotMessageIn
from app.core.settings import settings

router = APIRouter()

# URL base da API do Telegram para enviar respostas
TELEGRAM_API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"

async def enviar_resposta_telegram(chat_id: int, text: str):
    """Envia a resposta de texto de volta ao utilizador no Telegram."""
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                TELEGRAM_API_URL,
                json={"chat_id": chat_id, "text": text},
                timeout=10
            )
        except Exception as e:
            print(f"Erro ao enviar resposta para o Telegram (ChatID {chat_id}): {e}")

@router.post("/webhook/telegram", include_in_schema=False)
async def handle_telegram_webhook(request: Request):
    """Endpoint principal que recebe as atualizações (mensagens) do Telegram."""
    data = {}
    chat_id = None
    try:
        data = await request.json()
        print(f"Webhook do Telegram recebido: {data}")

        message = data.get("message")
        if not message:
            return {"status": "ignorado (não é mensagem)"}

        chat_id = message.get("chat", {}).get("id")
        text = message.get("text")
        user_id = message.get("from", {}).get("id")

        if not chat_id or not text or not user_id:
            return {"status": "ignorado (dados em falta)"}

        print(f"Mensagem recebida do Telegram (ChatID {chat_id}): {text}")

        # 1. TRADUZ para o nosso formato interno (BotMessageIn)
        mensagem_entrada = BotMessageIn(
            user_id=str(user_id), # O nosso serviço espera uma string
            text=text
        )

        # 2. CHAMA O NOSSO CÉREBRO
        resposta_bot = await bot_service.processar_mensagem(mensagem_entrada)

        # 3. ENVIA A RESPOSTA de volta ao Telegram
        await enviar_resposta_telegram(
            chat_id=chat_id,
            text=resposta_bot.response_text
        )

    except Exception as e:
        print(f"Erro grave no processamento do webhook do Telegram: {e}")
        if chat_id:
            await enviar_resposta_telegram(chat_id, "Desculpe, ocorreu um erro interno.")
            
    finally:
        # 4. Responde 200 OK ao Telegram IMEDIATAMENTE.
        return {"status": "ok"}