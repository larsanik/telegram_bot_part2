from dataclasses import dataclass

from app.infra.postgres.db import Database

from app.core.users.models import User
from sqlalchemy.dialects.postgresql import insert

@dataclass
class UserRepository:
    database: Database

    async def create_user_if_not_exists(self, user_id: int, is_waiter: bool = False) -> None:
        async with self.database.session() as conn:
            insert_stmt = insert(User).values(id=user_id, is_waiter=is_waiter).on_conflict_do_nothing()
            await conn.execute(insert_stmt)
            await conn.commit()
