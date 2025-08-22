from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class DeleteGenreInput:
    id: UUID


class DeleteGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository
    
    def execute(self, input: DeleteGenreInput) -> None:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with id {input.id} not found.")
        
        self.repository.delete(genre.id)

 