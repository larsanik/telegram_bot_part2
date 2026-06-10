from dataclasses import dataclass

from app.core.orders.constants import OrderStatusEnum
from app.core.orders.models import Order, Product
from app.core.orders.repositories import ProductRepository


@dataclass
class ProductService:
    repository: ProductRepository

    async def list_products(self) -> list[Product]:
        return await self.repository.list_products()