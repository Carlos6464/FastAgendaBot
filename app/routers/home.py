from fastapi import APIRouter

# 1. Criamos um "Router".
# Pense nisso como um "mini-app" do FastAPI,
# que pode ser "plugado" no app principal.
router = APIRouter()

# 2. Definimos a rota neste router
@router.get("/")
async def raiz():
    # 3. A mesma lógica que tínhamos antes
    return {"message": "Olá, Mundo! direto do nosso CONTROLLER!"}