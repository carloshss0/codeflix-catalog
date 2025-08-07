from src.core.category.application.update_category import UpdateCategory, UpdateCategoryInput
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        
        category_movie = Category(
                name = "Movie",
                description="Category for movies",
                is_active=True,
            )

        repository = InMemoryCategoryRepository()

        repository.save(category_movie)
        use_case = UpdateCategory(repository=repository)

        input = UpdateCategoryInput(
            id=category_movie.id,
            name="Updated Movie",
            description="Updated description for movies",
        )

        use_case.execute(input)

        assert category_movie.name == "Updated Movie"
        assert category_movie.description == "Updated description for movies"
        assert category_movie.is_active is True
        assert len(repository.categories) == 1

    def test_can_update_category_activation_status(self):
        category_movie = Category(
            name = "Movie",
            description="Category for movies",
            is_active=True,
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        use_case = UpdateCategory(repository=repository)

        input = UpdateCategoryInput(
            id=category_movie.id,
            is_active=False,
        )

        use_case.execute(input)
        assert category_movie.name == "Movie"
        assert category_movie.description == "Category for movies"
        assert category_movie.is_active is False
        assert len(repository.categories) == 1