import uvicorn
from fastapi import FastAPI

from db.database import engine, Base, async_session_maker
from src.router import router
from src.service import UserService

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        user_service = UserService(session)
        loaded_users = await user_service.load_users_from_api(1000)
        await user_service.save_users_to_db(loaded_users)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000
    )
