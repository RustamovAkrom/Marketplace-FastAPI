# src/api/v1/upload.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core import config
from db.crud.base import get_crud_for_model  # универсальная функция для CRUD
from db.dependencies.sessions import get_db_session
from services.file_service import save_file

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/{model_name}/{instance_id}/{field_name}")
async def upload_file(
    model_name: str,
    instance_id: int,
    field_name: str,
    file: UploadFile,
    filetype: str = "image",
    db: AsyncSession = Depends(get_db_session),
):
    """
    Универсальный upload endpoint.
    model_name: имя модели в lower_case
    instance_id: ID объекта
    field_name: имя поля модели для сохранения пути
    """
    # Получаем CRUD для модели
    crud = get_crud_for_model(model_name, db)
    if not crud:
        raise HTTPException(
            status_code=400, detail=f"Model '{model_name}' not supported"
        )

    # Получаем объект
    instance = await crud.get_by_id(instance_id)
    if not instance:
        raise HTTPException(
            status_code=404, detail=f"{model_name.capitalize()} not found"
        )

    # Сохраняем файл
    relative_path = await save_file(file, model_name, instance_id, filetype)

    # Обновляем поле модели
    current_value = getattr(instance, field_name, None)
    if isinstance(current_value, list):
        # для множественных файлов
        current_value.append(relative_path)
        setattr(instance, field_name, current_value)
    else:
        # одно поле
        setattr(instance, field_name, relative_path)

    db.add(instance)
    await db.commit()
    await db.refresh(instance)

    return {"url": f"{config.MEDIA_URL}{relative_path}", "field": field_name}
