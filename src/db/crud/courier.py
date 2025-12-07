# # src/db/crud/courier.py
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from db.models.courier_profile import CourierProfile
# from schemas.courier import CourierCreateScheme, CourierUpdateLocationScheme


# class CourierCRUD:
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def get_by_user_id(self, user_id: int):
#         stmt = select(CourierProfile).where(CourierProfile.user_id == user_id)
#         res = await self.session.execute(stmt)
#         return res.scalars().first()

#     async def create(self, user_id: int, data: CourierCreateScheme):
#         courier = CourierProfile(
#             user_id=user_id,
#             transport_type=data.transport_type,
#         )
#         self.session.add(courier)
#         await self.session.commit()
#         await self.session.refresh(courier)
#         return courier

#     async def update_location(self, courier: CourierProfile, lat: float, lon: float):
#         courier.latitude = lat
#         courier.longitude = lon
#         await self.session.commit()
#         return courier

#     async def set_availability(self, courier: CourierProfile, available: bool):
#         courier.is_available = available
#         await self.session.commit()
#         return courier
