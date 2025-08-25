from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GetGenreInput:
    id: UUID

@dataclass
class GetGenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class GetGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository
    
    def execute(self, input: GetGenreInput) -> GetGenreOutput:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with id {input.id} not found.")
        
        return GetGenreOutput(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories
        )