from src.service import UserService


async def test_get_random_user(user_service: UserService):
    random_user1 = await user_service.get_random_user()
    assert random_user1 is not None and random_user1.id > 0

    random_user2 = await user_service.get_random_user()
    assert random_user2 is not None and random_user2.id > 0

    while random_user2 == random_user1:
        random_user2 = await user_service.get_random_user()
    assert random_user2 != random_user1
