from uuid import UUID
import uuid

import pytest
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.get_genre import GetGenre, GetGenreInput, GetGenreOutput
from src.core.genre.domain.genre import Genre
from src.core.genre.infrastructure.in_memory_genre_repository import InMemoryGenreRepository
from src.core.category.domain.category import Category
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestGetGenre:
    def test_get_category_by_id(self):
        category_movie = Category(
            name = "Movie",
            description="Category for movies",
            is_active=True,
        )

        category_documentary = Category(
            name = "Documentary",
            description="Category for documentaries",
            is_active=True,
        )

        category_repository = InMemoryCategoryRepository()
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        repository = InMemoryGenreRepository()

        genre = Genre(
            name = "Action",
            categories = {category_movie.id, category_documentary.id}
        )

        repository.save(genre)
        
        use_case = GetGenre(repository=repository)
        
        input = GetGenreInput(
            id = genre.id,
        )

        output = use_case.execute(input)

        assert output == GetGenreOutput(
            id=genre.id,
            name="Action",
            is_active=True,
            categories={category_movie.id, category_documentary.id}
        )

    def test_get_category_when_it_does_not_exist(self):
        repository = InMemoryGenreRepository()
        use_case = GetGenre(repository=repository)
        input = GetGenreInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(GenreNotFound, match=f"Genre with id {input.id} not found."):
            use_case.execute(input)

