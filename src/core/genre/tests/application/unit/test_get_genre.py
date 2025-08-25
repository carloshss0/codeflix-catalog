from unittest.mock import MagicMock
import uuid
import pytest
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.get_genre import GetGenre, GetGenreInput
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository


class TestGetGenre:
    def test_get_genre_successfully(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_active=True)
        
        mock_category_repository = MagicMock(CategoryRepository)
        mock_category_repository.list.return_value = [category]


        genre = Genre(
            name="Test Genre",
            is_active=True,
            categories = {category.id}
            )
        
        mock_genre_repository = MagicMock(GenreRepository)
        mock_genre_repository.get_by_id.return_value = genre

        use_case = GetGenre(
            repository=mock_genre_repository
        )
        input = GetGenreInput(
            id= category.id,  # Assuming UUID is generated here for the test
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert mock_genre_repository.get_by_id.called is True

    def test_get_genre_when_it_does_not_exist(self):
        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = None
        use_case = GetGenre(
            repository=mock_repository
        )

        input = GetGenreInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(GenreNotFound, match=f"Genre with id {input.id} not found."):
            use_case.execute(input)