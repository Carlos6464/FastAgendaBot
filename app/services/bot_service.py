# Em app/services/bot_service.py
from app.schemas import BotMessageIn, BotMessageOut

# Esta função é o "cérebro". Ela recebe a mensagem validada
# e decide o que fazer com ela.
async def processar_mensagem(mensagem: BotMessageIn) -> BotMessageOut:
    
    # --- LÓGICA DO BOT COMEÇA AQUI ---
    
    # Por enquanto, nossa lógica é burra:
    # Vamos apenas "ecoar" a mensagem de volta
    resposta = f"Você disse: '{mensagem.text}'"
    
    # --- LÓGICA DO BOT TERMINA AQUI ---
    
    # Retornamos o objeto de resposta formatado
    return BotMessageOut(
        user_id=mensagem.user_id,
        response_text=resposta
    )