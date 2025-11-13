from fastapi import FastAPI
from app.routers import home
from app.routers import bot_webhook
from app.routers import telegram_webhook

app = FastAPI(
    title="FastAgenda Bot",
    description="API para o chatbot de agendamento."
)

# Inclui os routers
app.include_router(home.router, tags=["Home"])
app.include_router(
    bot_webhook.router, 
    prefix="/api/v1", 
    tags=["Chatbot (Teste)"]
)
app.include_router(
    telegram_webhook.router,
    tags=["Webhooks"]
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}