# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from core.security import (
#     create_access_token,
#     create_refresh_token,
#     hash_password,
#     verify_password,
# )
# from db.crud.user import UserCRUD


# class AuthService:
#     def __init__(self, session: AsyncSession):
#         self.session = session
#         self.user_crud = UserCRUD(session)

#     async def register(self, data):
#         user = await self.user_crud.get_by_email(data.email)
#         if user:
#             raise HTTPException(status_code=400, detail="Email already registered")

#         hashed = hash_password(data.password)

#         new_user = await self.user_crud.create(
#             email=data.email,
#             username=data.username,
#             password=hashed,
#         )

#         return {
#             "access_token": create_access_token({"sub": str(new_user.id)}),
#             "refresh_token": create_refresh_token({"sub": str(new_user.id)}),
#             "token_type": "bearer",
#         }

#     async def login(self, data):
#         user = await self.user_crud.get_by_email(data.email)
#         if not user or not verify_password(data.password, user.password):
#             raise HTTPException(status_code=401, detail="Incorrect credentials")

#         return {
#             "access_token": create_access_token({"sub": str(user.id)}),
#             "refresh_token": create_refresh_token({"sub": str(user.id)}),
#             "token_type": "bearer",
#         }

#     async def refresh(self, token: str):
#         # токен уже проверяется в зависимостях
#         return {
#             "access_token": create_access_token({"sub": token["sub"]}),
#             "refresh_token": create_refresh_token({"sub": token["sub"]}),
#             "token_type": "bearer",
#         }
