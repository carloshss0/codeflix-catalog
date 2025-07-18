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

    def test_can_delete_category_by_id(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = InMemoryCategoryRepository(categories=[category])

        repository.delete(category.id)
        assert len(repository.categories) == 0

    def test_delete_category_by_id_does_nothing_if_not_found(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = InMemoryCategoryRepository(categories=[category])

        non_existent_id = uuid.uuid4()
        repository.delete(non_existent_id)
        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_can_update_category(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = InMemoryCategoryRepository(categories=[category])

        updated_category = Category(
            id=category.id,
            name="Updated Category",
            description="This is an updated category",
            is_activate=False
        )
        repository.update(updated_category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == updated_category

    def test_update_category_does_nothing_if_not_found(self):
        category = Category(
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = InMemoryCategoryRepository(categories=[category])

        non_existent_category = Category(
            id=uuid.uuid4(),
            name="Non-existent Category",
            description="This category does not exist",
            is_activate=False
        )
        repository.update(non_existent_category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_can_list_categories(self):
        category1 = Category(
            name="Category 1",
            description="First category",
            is_activate=True
        )
        category2 = Category(
            name="Category 2",
            description="Second category",
            is_activate=False
        )
        repository = InMemoryCategoryRepository(categories=[category1, category2])

        categories = repository.list()
        assert len(categories) == 2
        assert categories[0] == category1
        assert categories[1] == category2