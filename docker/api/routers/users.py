from typing import List, Tuple
from fastapi import Depends, APIRouter, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.users as users_model
import api.schemas.users as users_schema
import api.cruds.users as users_cruds
from api.db import get_db

router = APIRouter()

# @router.get("/users")
# async def list_users(db: AsyncSession = Depends(get_db)) -> List[Tuple[int, str, str, str, str, bool]]:
#     result: Result = await db.execute(
#         select(
#             users_model.User.id,
#             users_model.User.username,
#             users_model.User.full_name,
#             users_model.User.email,
#             users_model.User.hashed_password,
#             users_model.User.disabled
#         )
#     )
#     return result.all()

@router.get("/users", response_model=List[users_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await users_cruds.get_users(db)
