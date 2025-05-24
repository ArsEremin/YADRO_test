import pytest

from src.service import UserService


@pytest.mark.parametrize(
    "user_id, gender, first_name, last_name, email, is_exist",
    [
        (1, "male", "John", "Abrams", "john@test.com", True),
        (2, "male", "Ivan", "Petrov", "ivan@test.com", True),
        (3, "female", "Vika", "Sidorova", "vika@test.com", True),
        (100, "invalid", "Invalid", "Invalid", "invalid@test.com", False),
    ]
)
async def test_get_user_by_id(user_service: UserService, user_id, gender, first_name, last_name, email, is_exist):
    user = await user_service.get_user_by_id(user_id)

    if is_exist:
        assert user.id == user_id and user.gender == gender and user.first_name == first_name \
               and user.last_name == last_name and user.email == email
    else:
        assert user is None
