from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from db.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.api_url = "https://randomuser.me/api"

    async def get_user_by_id(self, user_id: int):
        query = select(User).filter_by(id=user_id)
        res = await self._session.execute(query)
        return res.scalar()

    async def get_random_user(self):
        query = select(User).order_by(func.random()).limit(1)
        res = await self._session.execute(query)
        return res.scalar()

    async def get_users_with_limit(self, page: int = 1, per_page: int = 10):
        offset = (page - 1) * per_page
        query = select(User).offset(offset).limit(per_page)
        res = await self._session.execute(query)
        users = res.scalars().all()
        total = await self._session.scalar(select(func.count(User.id)))
        return users, total

    async def load_users_from_api(self, users_num: int):
        async with httpx.AsyncClient() as async_client:
            response = await async_client.get(f"{self.api_url}/?results={users_num}")
            return response.json()["results"]

    async def save_users_to_db(self, users_data: list[dict]):
        for user_data in users_data:

            user = User(
                **{
                    "gender": user_data["gender"],
                    "first_name": user_data["name"]["first"],
                    "last_name": user_data["name"]["last"],
                    "phone": user_data["phone"],
                    "email": user_data["email"],
                    "location": f"{user_data['location']['country']}, {user_data['location']['city']}",
                    "photo": user_data["picture"]["thumbnail"],
                    "profile_url": "temp_url"
                }
            )

            self._session.add(user)
            await self._session.flush()
            user.profile_url = f"/user/{user.id}"
            await self._session.commit()


async def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
    return UserService(session)
