from uuid import UUID
import uuid

import pytest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryInput
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_by_id(self):
        category_movie = Category(
            name = "Movie",
            description="Category for movies",
            is_activate=True,
        )

        category_documentary = Category(
            name = "Documentary",
            description="Category for documentaries",
            is_activate=True,
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)
        use_case = DeleteCategory(repository=repository)
        
        input = DeleteCategoryInput(
            id = category_movie.id,
        )
        assert repository.get_by_id(input.id) == category_movie
        use_case.execute(input)

        assert repository.get_by_id(input.id) is None

    def test_delete_category_when_it_does_not_exist(self):

        repository = InMemoryCategoryRepository()
        use_case = DeleteCategory(repository=repository)
        input = DeleteCategoryInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(CategoryNotFound):
            use_case.execute(input)
        
        assert repository.get_by_id(input.id) is None


        
