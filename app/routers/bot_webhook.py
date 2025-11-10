# Em app/routers/bot_webhook.py
from fastapi import APIRouter, Depends
from app.schemas import BotMessageIn, BotMessageOut
from app.services import bot_service

router = APIRouter()

# 1. Definimos a rota como POST /webhook
# 2. 'response_model=BotMessageOut' diz ao FastAPI para formatar
#    a saída de acordo com nosso schema.
@router.post("/webhook", response_model=BotMessageOut)
async def handle_webhook(
    # 3. Mágica do FastAPI:
    # Ele pega o corpo (body) do POST, valida contra o
    # BotMessageIn, e nos entrega como um objeto Python.
    # Se a validação falhar (ex: 'user_id' faltar), o FastAPI
    # retorna um erro 422 automático.
    mensagem: BotMessageIn
):
    # 4. O Controller NÃO FAZ LÓGICA.
    # Ele apenas delega para o Service.
    resposta = await bot_service.processar_mensagem(mensagem)
    
    return resposta