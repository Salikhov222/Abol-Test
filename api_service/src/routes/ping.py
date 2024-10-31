from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get('/app')
async def ping_app():
    return {"app": "ok"}

@router.get('/db')
async def ping_db():
    return {"db": "ok"}