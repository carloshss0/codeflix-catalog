from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.category.application.category_repository import CategoryRepository

@dataclass
class CreateGenreInput:
    name: str
    categories_ids: set[UUID] = field(default_factory=set)
    is_active: bool = True

@dataclass
class CreateGenreOutput:
    id: UUID

class CreateGenre:
    def __init__(self, repository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    def execute(self, input: CreateGenreInput) -> CreateGenreOutput:
        categories_ids = {category.id for category in self.category_repository.list()}

        if not input.categories_ids.issubset(categories_ids):
            raise RelatedCategoriesNotFound(
                f"Category id not found: {input.categories_ids - categories_ids}"
            )
        
        try:
            genre = Genre(
                name= input.name,
                categories =  input.categories_ids,
                is_active= input.is_active
            )
        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.save(genre)

        return CreateGenreOutput(genre.id)



