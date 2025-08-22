from uuid import UUID
import uuid

import pytest
from src.core.genre.application.delete_genre import DeleteGenre, DeleteGenreInput
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.infrastructure.in_memory_genre_repository import InMemoryGenreRepository
from src.core.category.domain.category import Category
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteGenre:
    def test_delete_genre_by_id(self):
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


        drama_genre = Genre(
            name="Drama",
            categories={category_movie.id, category_documentary.id}
        )
        genre_repository = InMemoryGenreRepository()
        genre_repository.save(drama_genre)
        
        use_case = DeleteGenre(repository=genre_repository)

        input = DeleteGenreInput(
            id = drama_genre.id,
        )

        assert genre_repository.get_by_id(input.id) == drama_genre
        use_case.execute(input)

        assert genre_repository.get_by_id(input.id) is None

    def test_delete_genre_when_it_does_not_exist(self):

        repository = InMemoryGenreRepository()
        use_case = DeleteGenre(repository=repository)
        input = DeleteGenreInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(input)
        
        assert repository.get_by_id(input.id) is None


        
