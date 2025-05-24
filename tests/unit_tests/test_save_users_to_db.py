from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from src.service import UserService


async def test_save_users_to_db(
    session: AsyncSession,
    user_service: UserService,
    mock_user_data: dict
):
    users_num = 10
    mock_users_data = [mock_user_data] * users_num

    await user_service.save_users_to_db(mock_users_data)

    saved_users = (await session.execute(select(User))).scalars().all()
    assert len(saved_users) == users_num + 3
    user = saved_users[3]
    assert user.first_name == "Alex"
    assert user.last_name == "Ivanov"
    assert user.email == "john@mock.com"
    assert user.phone == "123-456-789"
