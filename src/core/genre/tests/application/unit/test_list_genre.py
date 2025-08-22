from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.genre.application.list_genre import ListGenreInput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.category.application.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category):
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestCreateGenre:
    def test_list_genre_with_categories(
        self,
        mock_genre_repository,
        movie_category,
        documentary_category
    ):

        list_genre = [
            Genre(
                name="Drama",
                categories={movie_category.id, documentary_category.id}
            ),
            Genre(
                name="Fiction",
                categories={movie_category.id, documentary_category.id}
            )
        ]
        mock_genre_repository.list.return_value = list_genre
        use_case = ListGenre(repository=mock_genre_repository)
        input = ListGenreInput()

        output = use_case.execute(input=input)
        assert len(output.data) == 2
        assert output.data[0].name == "Drama"
        assert output.data[1].name == "Fiction"
        assert output.data[0].categories == {movie_category.id, documentary_category.id}
        assert output.data[1].categories == {movie_category.id, documentary_category.id}

    def test_list_when_no_genres_exist(
        self,
        mock_genre_repository
    ):
        mock_genre_repository.list.return_value = []
        use_case = ListGenre(repository=mock_genre_repository)
        input = ListGenreInput()

        output = use_case.execute(input=input)

        assert len(output.data) == 0

