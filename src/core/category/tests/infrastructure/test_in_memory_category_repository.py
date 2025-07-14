import uuid
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
    
    def test_can_get_category_by_id(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = InMemoryCategoryRepository(categories=[category])

        retrieved_category = repository.get_by_id(category.id)
        assert retrieved_category == category
    
    def test_get_category_by_id_returns_none_if_not_found(self):
        repository = InMemoryCategoryRepository()
        category_id = uuid.uuid4()
        retrieved_category = repository.get_by_id(category_id)

        assert retrieved_category is None