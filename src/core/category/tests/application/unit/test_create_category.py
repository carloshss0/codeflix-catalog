from unittest.mock import MagicMock
import pytest
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryInput
from src.core.category.application.exceptions import InvalidCategoryData

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(
            repository=mock_repository
        )
        input = CreateCategoryInput(
            name="Test Category",
            description="This is a test category",
            is_active=True  # Default
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(
            repository=mock_repository
        )
        with pytest.raises(InvalidCategoryData, match="name cannot be empty"):
            output = use_case.execute(
                CreateCategoryInput(
                    name="",  # Invalid name
                )
            )