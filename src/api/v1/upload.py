from fastapi import APIRouter, UploadFile

from services.file_service import FileService

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image")
async def upload_image(file: UploadFile):
    url = await FileService.save_image(file, "uploads")
    return {"url": url}
