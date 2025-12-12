import uvicorn

from core.settings import settings

if __name__ == "__main__":

    uvicorn.run(
        "app:create_app",
        app_dir="src",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
