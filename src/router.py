from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.service import UserService, get_user_service

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def homepage(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    page: int = 1,
    per_page: int = 10
):
    users, total = await user_service.get_users_with_limit(page, per_page)
    return templates.TemplateResponse(
        "homepage.html",
        {
            "request": request,
            "users": users,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    )


@router.post("/")
async def load_users(
    users_num: Annotated[int, Form()],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    loaded_users = await user_service.load_users_from_api(users_num)
    await user_service.save_users_to_db(loaded_users)

    return RedirectResponse(url="/?page=1", status_code=303)


@router.get("/random")
async def get_random_user(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    random_user = await user_service.get_random_user()
    return templates.TemplateResponse("user_profile.html", {"request": request, "user": random_user})


@router.get("/{profile_url:path}")
async def get_user_profile(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    profile_url: str
):
    user_id = profile_url.split('/')[-1]
    user = await user_service.get_user_by_id(int(user_id))
    return templates.TemplateResponse("user_profile.html", {"request": request, "user": user})
