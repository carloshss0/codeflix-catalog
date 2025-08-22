from unittest.mock import create_autospec
import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.update_genre import UpdateGenre, UpdateGenreInput
from src.core.category.domain.category import Category
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
def mock_category_repository(movie_category, documentary_category):
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository



class TestUpdateGenre:
    def test_update_genre_with_valid_data(
        self,
        mock_genre_repository,
        mock_category_repository,
        movie_category,
        documentary_category
    ):
        genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository

        )

        input = UpdateGenreInput(
            id=genre.id,
            name="Updated Drama",
            categories={documentary_category.id},
            is_active=True
        )

        use_case.execute(input)

        assert genre.name == "Updated Drama"
        assert genre.categories == {documentary_category.id}
        assert genre.is_active is True
        mock_genre_repository.update.assert_called_once_with(genre)

    def test_update_genre_with_invalid_name(
        self,
        mock_genre_repository,
        mock_category_repository,
        movie_category,
        documentary_category
    ):
        genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository
        )

        input = UpdateGenreInput(
            id=genre.id,
            name="",  # Invalid name
            categories={documentary_category.id},
            is_active=True
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input)

    def test_update_genre_with_non_existent_id(
        self,
        mock_genre_repository,
        mock_category_repository
    ):
        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository
        )

        input = UpdateGenreInput(
            id=uuid.uuid4(),  # Non-existent ID
            name="Updated Drama",
            categories=set(),
            is_active=True
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(input)


    def test_update_genre_with_invalid_categories(
        self,
        mock_genre_repository,
        mock_category_repository,
        movie_category
    ):
        genre = Genre(
            name="Drama",
            categories={movie_category.id}
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository
        )

        input = UpdateGenreInput(
            id=genre.id,
            name="Updated Drama",
            categories={uuid.uuid4()},  # Invalid category ID
            is_active=True
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

