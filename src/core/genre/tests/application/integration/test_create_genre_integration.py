from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infrastructure.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.application.create_genre import CreateGenre, CreateGenreInput
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.domain.genre_repository import GenreRepository
from src.django_project.category_app.models import Category

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category,
        documentary_category
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])


        use_case = CreateGenre(
            repository = genre_repository,
            category_repository= category_repository
        )

        input = CreateGenreInput(
            name= "Action",
            categories= {movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)

        assert output is not None
        assert isinstance(output.id, uuid.UUID)
        assert len(genre_repository.genres) == 1
        assert genre_repository.genres[0].id == output.id

    def test_create_genre_with_non_existent_categories(
        self,
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        non_existent_category_id = uuid.uuid4()

        use_case = CreateGenre(
            repository= genre_repository,
            category_repository= category_repository,
        )

        input = CreateGenreInput(
            name= "Action",
            categories= {non_existent_category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    
    def test_create_genre_with_invalid_name(
        self,
        movie_category,
        documentary_category,   
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])

        use_case = CreateGenre(
            repository= genre_repository,
            category_repository= category_repository
        )

        input = CreateGenreInput(
            name= "",
            categories= {movie_category.id, documentary_category.id}
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input)

    def test_create_genre_without_categories(self):

        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        use_case = CreateGenre(
            repository= genre_repository,
            category_repository=category_repository
        )

        input = CreateGenreInput(
            name= "Action"    
        )

        output = use_case.execute(input)

        assert output is not None
        assert isinstance(output.id, uuid.UUID)

        assert len(genre_repository.genres) == 1
        assert genre_repository.genres[0].id == output.id