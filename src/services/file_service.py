import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from core.config import settings

ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]


class FileService:

    @staticmethod
    async def save_image(file: UploadFile, folder: str) -> str | None:
        # Проверка типа файла
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="Файл должен быть изображением")

        # Генерация уникального имени файла
        if file.filename:
            ext = file.filename.split(".")[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

        # Папка для сохранения
        save_dir = Path(settings.MEDIA_ROOT) / folder
        save_dir.mkdir(parents=True, exist_ok=True)

        # Полный путь на сервере
        file_path = save_dir / filename

        # Сохраняем файл
        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Не удалось сохранить файл: {e}"
            )

        # Возвращаем путь для фронтенда
        return f"{settings.MEDIA_URL}/{folder}/{filename}"
