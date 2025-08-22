from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound



@dataclass
class UpdateGenreInput:
    id: UUID
    name: str | None = None
    categories: set[UUID] | None = None
    is_active: bool | None = None
    

class UpdateGenre:
    def __init__(self, genre_repository: GenreRepository, category_repository: CategoryRepository):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    def execute(self, input: UpdateGenreInput) -> None:
        genre = self.genre_repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with id {input.id} not found.")

        # current_name = genre.name
        # current_categories = genre.categories
        # current_is_active = genre.is_active

        try:
            if input.name is not None:
                genre.change_name(input.name)

            if input.is_active is not None:
                if input.is_active is True:
                    genre.activate()
                else:
                    genre.deactivate()
        except ValueError as e:
            raise InvalidGenre(e)


        if input.categories is not None:
            categories_ids = {category.id for category in self.category_repository.list()}
            if not input.categories.issubset(categories_ids):
                raise RelatedCategoriesNotFound(
                    f"Category id not found: {input.categories - categories_ids}"
                )
            
            for category_id in genre.categories - input.categories:
                genre.remove_category(category_id)
            
            for category_id in input.categories - genre.categories:
                genre.add_category(category_id)



        self.genre_repository.update(genre)