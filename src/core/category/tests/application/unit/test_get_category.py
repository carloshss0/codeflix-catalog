from unittest.mock import MagicMock
import uuid
import pytest
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.get_category import GetCategory, GetCategoryInput
from src.core.category.application.exceptions import CategoryNotFound

class TestGetCategory:
    def test_get_category_successfully(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_active=True)
        
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(
            repository=mock_repository
        )
        input = GetCategoryInput(
            id= category.id,  # Assuming UUID is generated here for the test
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert mock_repository.get_by_id.called is True

    def test_get_category_when_it_does_not_exist(self):
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = GetCategory(
            repository=mock_repository
        )

        input = GetCategoryInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(CategoryNotFound, match=f"Category with id {input.id} not found."):
            use_case.execute(input)