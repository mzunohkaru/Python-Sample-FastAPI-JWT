from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.users as users_model



async def get_users(db: AsyncSession) -> List[Tuple[int, str, str, str, str, bool]]:
    result: Result = await db.execute(
        select(
            users_model.User.id,
            users_model.User.username,
            users_model.User.full_name,
            users_model.User.email,
            users_model.User.hashed_password,
            users_model.User.disabled
        )
    )
    return result.all()