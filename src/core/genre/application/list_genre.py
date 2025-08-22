from dataclasses import dataclass
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class ListGenreInput:
    pass

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

@dataclass
class ListGenreOutput:
    data: list[GenreOutput]

class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: ListGenreInput):
        genres = self.repository.list()

        return ListGenreOutput(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories
                ) for genre in genres
            ]
        )