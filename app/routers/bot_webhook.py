# Em app/routers/bot_webhook.py
from fastapi import APIRouter, Depends
from app.schemas import BotMessageIn, BotMessageOut
from app.services import bot_service

router = APIRouter()

@router.post("/webhook", response_model=BotMessageOut)
async def handle_webhook(mensagem: BotMessageIn):
    resposta = await bot_service.processar_mensagem(mensagem)
    return resposta