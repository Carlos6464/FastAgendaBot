from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def raiz():
    return {"message": "Olá, Mundo! direto do nosso CONTROLLER!"}