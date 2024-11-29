from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.routes import routers

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'detail': f'Произошла ошибка при обработке запроса {request.url}: {str(exc)}'}
    )

for router in routers:
    app.include_router(router)
