from uuid import UUID
import uuid

import pytest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.application.get_category import GetCategory, GetCategoryInput, GetCategoryOutput
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
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
        
        use_case = GetCategory(repository=repository)
        
        input = GetCategoryInput(
            id = category_movie.id,
        )

        output = use_case.execute(input)

        assert output == GetCategoryOutput(
            id=category_movie.id,
            name="Movie",
            description="Category for movies",
            is_active=True,
        )

    def test_get_category_when_it_does_not_exist(self):
        repository = InMemoryCategoryRepository()
        use_case = GetCategory(repository=repository)
        input = GetCategoryInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(CategoryNotFound, match=f"Category with id {input.id} not found."):
            use_case.execute(input)

