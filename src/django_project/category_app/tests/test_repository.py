from uuid import UUID

import pytest

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category(self):
        category = Category(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        assert CategoryModel.objects.count() == 0
        repository.save(category)

        category_db = CategoryModel.objects.get(id=category.id)
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_activate == category.is_activate
        assert CategoryModel.objects.count() == 1
    
    def test_get_category_by_id(self):
        category = Category(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category)

        retrieved_category = repository.get_by_id(category.id)
        assert retrieved_category is not None
        assert retrieved_category.id == category.id
        assert retrieved_category.name == category.name
        assert retrieved_category.description == category.description
        assert retrieved_category.is_activate == category.is_activate

    def test_delete_category(self):
        category = Category(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category)

        assert CategoryModel.objects.count() == 1
        repository.delete(category.id)
        assert CategoryModel.objects.count() == 0
    

    def test_list_categories(self):
        category1 = Category(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Test Category 1",
            description="This is a test category 1",
            is_activate=True
        )
        category2 = Category(
            id=UUID("87654321-4321-6789-4321-678987654321"),
            name="Test Category 2",
            description="This is a test category 2",
            is_activate=False
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category1)
        repository.save(category2)

        categories = repository.list()
        assert len(categories) == 2
        assert categories[0].id == category1.id
        assert categories[1].id == category2.id
    
    def test_update_category(self):
        category = Category(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Test Category",
            description="This is a test category",
            is_activate=True
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category)

        category.update_category(name="Updated Category", description="Updated description")
        updated_category = repository.update(category)

        assert updated_category.id == category.id
        assert updated_category.name == "Updated Category"
        assert updated_category.description == "Updated description"
        assert updated_category.is_activate == category.is_activate