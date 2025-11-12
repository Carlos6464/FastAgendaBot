from fastapi import FastAPI
from app.routers import home
from app.routers import bot_webhook # O nosso endpoint de teste (curl)
from app.routers import telegram_webhook # <-- 1. IMPORTE O NOVO ROUTER

app = FastAPI(
    title="FastAgenda Bot",
    description="API para o chatbot de agendamento."
)

app.include_router(home.router, tags=["Home"])
app.include_router(
    bot_webhook.router, 
    prefix="/api/v1", 
    tags=["Chatbot (Teste)"] # Mudámos a tag
)

# --- 2. INCLUA O NOVO ROUTER DO TELEGRAM ---
app.include_router(
    telegram_webhook.router,
    tags=["Webhooks"] # O Telegram não precisa do prefixo /api/v1
)
# -----------------------------------------------

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}