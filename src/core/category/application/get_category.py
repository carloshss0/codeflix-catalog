from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category import Category

@dataclass
class GetCategoryInput:
    id: UUID

@dataclass
class GetCategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, input: GetCategoryInput) -> GetCategoryOutput:
        category = self.repository.get_by_id(input.id)
        if not category:
            raise CategoryNotFound(f"Category with id {input.id} not found.")
        
        return GetCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_activate
        )