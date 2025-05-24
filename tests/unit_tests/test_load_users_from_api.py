from unittest import mock
from unittest.mock import patch, AsyncMock

from httpx import Response

from src.service import UserService


async def test_load_users_from_api(user_service: UserService, mock_user_data: dict):
    users_num = 5
    mock_users_data = [mock_user_data] * users_num
    mock_response = {"results": mock_users_data}
    mock_get = AsyncMock(return_value=Response(200, json=mock_response))

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value = AsyncMock(get=mock_get)

        res = await user_service.load_users_from_api(users_num)
    assert res == mock_users_data

    url = "https://randomuser.me/api/"

    expected_calls = [
        mock.call(),
        mock.call().__aenter__(),
        mock.call().__aenter__().get(f'{url}?results={users_num}'),
        mock.call().__aexit__(None, None, None)
    ]
    assert mock_client.mock_calls == expected_calls


