from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category

@dataclass
class ListCategoryInput:
    pass

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_activate: bool


@dataclass
class ListCategoryOutput:
    data: list[CategoryOutput]

class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, input: ListCategoryInput) -> ListCategoryOutput:
        categories = self.repository.list()
    
        
        return ListCategoryOutput(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_activate=category.is_activate
                ) for category in categories
            ]
        )
    