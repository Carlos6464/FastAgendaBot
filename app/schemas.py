# Em app/schemas.py
from pydantic import BaseModel
from typing import Optional # Usaremos para campos opcionais no futuro

# Define a estrutura de uma mensagem que NÓS esperamos receber
# Por enquanto, bem simples: só um ID de usuário e um texto
class BotMessageIn(BaseModel):
    user_id: str
    text: str

# Define a estrutura da resposta que NÓS vamos enviar
class BotMessageOut(BaseModel):
    user_id: str
    response_text: str