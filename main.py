from fastapi import FastAPI
from app.routers import home
from app.routers import bot_webhook  # 1. IMPORTE O NOVO ROUTER

app = FastAPI(
    title="FastAgenda Bot",
    description="API para o chatbot de agendamento."
)

# 2. INCLUA O ROUTER de home
app.include_router(home.router, tags=["Home"]) 

# 3. INCLUA O ROUTER do bot
# 'prefix="/api/v1"' é uma boa prática.
# Agora o endpoint será: /api/v1/webhook
app.include_router(
    bot_webhook.router, 
    prefix="/api/v1", 
    tags=["Chatbot"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}