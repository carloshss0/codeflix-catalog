from unittest.mock import create_autospec

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.list_category import CategoryOutput, ListCategory, ListCategoryInput, ListCategoryOutput
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_in_repository(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)
        input = ListCategoryInput()
        output = use_case.execute(input = input)

        assert output == ListCategoryOutput(data=[])
        assert mock_repository.list.called is True

    def test_when_categories_in_repository(self):
        mock_repository = create_autospec(CategoryRepository)

        list_category = [
            Category(
                name="Movie",
                description="Category for movies",
                is_activate=True
            ),
            Category(
                name="Documentary",
                description="Category for documentaries",
                is_activate=True
            )
        ]

        mock_repository.list.return_value = list_category
        use_case = ListCategory(repository=mock_repository)
        input = ListCategoryInput()
        output = use_case.execute(input = input)

        assert output == ListCategoryOutput(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_activate
                ) for category in list_category
            ]
        )

        assert mock_repository.list.called is True
        assert len(output.data) == 2