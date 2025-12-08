import uvicorn

from app import create_app
from core.config import settings

if __name__ == "__main__":
    app = create_app()

    uvicorn.run(
        app=app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD and settings.ENV == "dev",
    )
