# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.db.dependencies import get_db_session
# from src.db.crud.category import CategoryCRUD
# from src.schemas.category import CategoryCreateScheme, CategoryUpdateScheme, CategoryOutScheme

# router = APIRouter()

# @router.get("/", response_model=list[CategoryOutScheme])
# async def list_categories(
#     category: AsyncSession = Depends(get_session)):
#     return await category_crud.get_all(session)

# @router.post("/", response_model=CategoryOutScheme)
# async def create_category(data: CategoryCreate, session: AsyncSession = Depends(get_session)):
#     existing = await category_crud.get_by_slug(session, data.slug)
#     if existing:
#         raise HTTPException(status_code=400, detail="Slug already exists")
#     return await category_crud.create(session, data)

# @router.get("/{category_id}", response_model=CategoryOutScheme)
# async def get_category(category_id: int, session: AsyncSession = Depends(get_session)):
#     category = await category_crud.get_by_id(session, category_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Not found")
#     return category

# @router.put("/{category_id}", response_model=CategoryOutScheme)
# async def update_category(
#     category_id: int,
#     data: CategoryUpdate,
#     session: AsyncSession = Depends(get_session)
# ):
#     category = await category_crud.get_by_id(session, category_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Not found")

#     return await category_crud.update(session, category, data)

# @router.delete("/{category_id}")
# async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
#     category = await category_crud.get_by_id(session, category_id)
#     if not category:
#         raise HTTPException(status_code=404, detail="Not found")

#     await category_crud.delete(session, category)
#     return {"status": "deleted"}
