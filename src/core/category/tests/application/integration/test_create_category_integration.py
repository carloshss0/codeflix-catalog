from uuid import UUID
from src.core.category.application.create_category import CreateCategory, CreateCategoryInput
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        input = CreateCategoryInput(
            name="Test Category",
            description="This is a test category",

        )
        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == output.id
        assert repository.categories[0].name == "Test Category"
        assert repository.categories[0].description == "This is a test category"

