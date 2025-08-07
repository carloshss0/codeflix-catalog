from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.domain.category import Category

@dataclass
class CreateCategoryInput:
    name: str
    description: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryOutput:
    id: UUID


class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, input: CreateCategoryInput) -> CreateCategoryOutput:
        try:
            category = Category(
                name=input.name,
                description=input.description,
                is_active=input.is_active
            )
        except ValueError as err:
            raise InvalidCategoryData(f"Invalid category data: {err}")

        self.repository.save(category)
        return CreateCategoryOutput(id=category.id)
 