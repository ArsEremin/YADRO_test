import asyncio
import json
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.config import settings
from db.database import Base
from db.models import User
from src.main import app as fastapi_app
from src.service import UserService


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
def test_db():
    settings.DB_NAME = "test_yadro_db"

    test_db_url = settings.database_uri_sync
    if not database_exists(test_db_url):
        create_database(test_db_url)

    try:
        yield settings.database_uri
    finally:
        drop_database(test_db_url)


@pytest.fixture(scope="session")
async def engine(test_db) -> AsyncEngine:
    async_engine = create_async_engine(test_db, future=True)
    yield async_engine
    await async_engine.dispose()


@pytest.fixture(scope="session")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def user_service(session: AsyncSession) -> UserService:
    return UserService(session)


@pytest.fixture(scope="session", autouse=True)
async def setup_db(engine):
    assert settings.DB_NAME == "test_yadro_db"

    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        with open(f"tests/test_data.json", 'r', encoding="utf-8") as file:
            values = json.load(file)

        await conn.execute(insert(User), values)
        await conn.commit()


@pytest.fixture(scope="session")
async def mock_user_data() -> dict:
    return {
        "gender": "male",
        "name": {"first": "Alex", "last": "Ivanov"},
        "phone": "123-456-789",
        "email": "john@mock.com",
        "location": {
            "country": "USA",
            "city": "New York",
            "street": {"number": 123, "name": "Avenue"},
            "postcode": "12345",
            "timezone": {"offset": "-4:00"}
        },
        "picture": {"thumbnail": "https://example.com/photo.jpg"},
        "login": {"uuid": "123e4567-e89b-12d3-a456-426614174000"}
    }
