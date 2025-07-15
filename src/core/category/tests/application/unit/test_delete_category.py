from unittest.mock import create_autospec
from uuid import UUID
import uuid
import pytest

from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryInput
from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.exceptions import CategoryNotFound

class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name = "Test Category",
            description = "Test Description",
            is_activate = True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = DeleteCategory(repository=mock_repository)
        usecase.execute(DeleteCategoryInput(category.id))
        mock_repository.delete.assert_called_once_with(category.id)

    def test_delete_category_with_invalid_id(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = DeleteCategory(
            repository=mock_repository
        )

        input = DeleteCategoryInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(CategoryNotFound):
            use_case.execute(input)
        
        mock_repository.get_by_id.assert_called_once_with(input.id)
        assert mock_repository.delete.called is False
