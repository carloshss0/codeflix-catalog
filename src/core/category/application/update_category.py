from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryInput:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    

class UpdateCategory:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, input: UpdateCategoryInput) -> None:
        category = self.repository.get_by_id(input.id)
        if not category:
            raise CategoryNotFound(f"Category with id {input.id} not found.")

        current_name = category.name
        current_description = category.description
        current_is_active = category.is_active

    
        if input.name is not None:
            current_name = input.name

        if input.description is not None:
            current_description = input.description

        if input.is_active is not None:
            current_is_active = input.is_active

        category.update_category(
            name=current_name,
            description=current_description,
        )

        if current_is_active is True:
            category.activate()
        elif current_is_active is False:
            category.deactivate()

        self.repository.update(category)