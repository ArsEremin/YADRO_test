import pytest

from src.service import UserService


@pytest.mark.parametrize(
    "page, per_page, expected_users_id",
    [
        (1, 1, [1]),
        (1, 2, [1, 2]),
        (2, 1, [2]),
        (2, 2, [3]),
        (1, 3, [1, 2, 3])
    ]
)
async def test_get_users_with_limit(
    user_service: UserService,
    page: int,
    per_page: int,
    expected_users_id: list[int]
):
    users, total = await user_service.get_users_with_limit(page, per_page)

    assert [user.id for user in users] == expected_users_id
    assert total == 3
