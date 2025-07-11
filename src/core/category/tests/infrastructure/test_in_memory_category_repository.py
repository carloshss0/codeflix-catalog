from src.core.category.domain.category import Category
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )

        repository.save(category)
        assert len(repository.categories) == 1
        assert repository.categories[0] == category