from dataclasses import dataclass
from app.core.orders.constants import OrderStatusEnum
from app.core.orders.models import Product
from app.infra.postgres.db import Database
from sqlalchemy import select, update, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert


@dataclass
class ProductRepository:
    database: Database

    async def list_products(self) -> list[Product]:
        async with self.database.session() as session:
            query = select(Product)
            return list(await session.scalars(query))
