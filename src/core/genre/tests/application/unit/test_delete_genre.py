from unittest.mock import create_autospec
from uuid import UUID
import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.delete_genre import DeleteGenre, DeleteGenreInput
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category import Category


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):

        category = Category(
            name = "Test Category",
            description = "Test Description",
            is_active = True,
        )

        genre = Genre(
            name = "Test Genre",
            categories={category.id}
        )

        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = genre

        usecase = DeleteGenre(repository=mock_repository)
        usecase.execute(DeleteGenreInput(genre.id))
        mock_repository.delete.assert_called_once_with(genre.id)

    def test_delete_genre_with_invalid_id(self):
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = None
        use_case = DeleteGenre(
            repository=mock_repository
        )

        input = DeleteGenreInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(GenreNotFound):
            use_case.execute(input)
        
        mock_repository.get_by_id.assert_called_once_with(input.id)
        assert mock_repository.delete.called is False
