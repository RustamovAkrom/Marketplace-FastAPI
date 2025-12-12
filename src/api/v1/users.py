from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from db.crud.user import UserCRUD
from db.dependencies.auth import require_admin
from schemas.user import UserOutScheme, UserUpdateScheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(require_admin),
    ],
)


@router.get("/", response_model=List[UserOutScheme])
async def get_users(users_crud: UserCRUD = Depends(UserCRUD)):
    users = await users_crud.all()
    return users


@router.get("/{user_id}", response_model=UserOutScheme)
async def get_user(user_id: int, users_crud: UserCRUD = Depends(UserCRUD)):
    user = await users_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserOutScheme)
async def update_user(
    user_id: int, data: UserUpdateScheme, users_crud: UserCRUD = Depends(UserCRUD)
):
    user = await users_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_data = data.dict(exclude_unset=True)
    user = await users_crud.update(user, **update_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, users_crud: UserCRUD = Depends(UserCRUD)):
    user = await users_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await users_crud.delete(user)
