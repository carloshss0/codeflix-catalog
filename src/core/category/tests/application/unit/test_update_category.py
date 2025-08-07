from unittest.mock import create_autospec
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryInput
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_active=True)
        
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository = mock_repository)
        input = UpdateCategoryInput(
            id=category.id,
            name="Updated Category Name",
        )
        
        use_case.execute(input)
        assert category.name == "Updated Category Name"
        assert category.description == "This is a test category"
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_called_once_with(category)


    def test_update_category_description(self):
        category = Category(
        name="Test Category",
        description="This is a test category",
        is_active=True)
        
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository = mock_repository)
        input = UpdateCategoryInput(
            id=category.id,
            description="Updated Category Description",
        )
        use_case.execute(input)

        assert category.name == "Test Category"
        assert category.description == "Updated Category Description"
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
        name="Test Category",
        description="This is a test category",
        is_active=True)
        
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository = mock_repository)
        input = UpdateCategoryInput(
            id=category.id,
            is_active= False,
        )
        use_case.execute(input)

        assert category.name == "Test Category"
        assert category.description == "This is a test category"
        assert category.is_active is False
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
        name="Test Category",
        description="This is a test category",
        is_active=False)
        
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository = mock_repository)
        input = UpdateCategoryInput(
            id=category.id,
            is_active= True,
        )
        use_case.execute(input)

        assert category.name == "Test Category"
        assert category.description == "This is a test category"
        assert category.is_active is True
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_called_once_with(category)