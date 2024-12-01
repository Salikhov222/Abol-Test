from src.routes.images import router as image_router
from src.routes.user import router as user_router
from src.routes.auth import router as auth_router

routers = [image_router, user_router, auth_router]