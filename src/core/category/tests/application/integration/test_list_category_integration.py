from src.core.category.application.list_category import CategoryOutput, ListCategory, ListCategoryInput, ListCategoryOutput
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category


class TestListCategory:
    def test_list_categories(self):
        category_movie = Category(
            name="Movie",
            description="Category for movies",
            is_activate=True,
        )
        category_documentary = Category(
            name="Documentary",
            description="Category for documentaries",
            is_activate=True,
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)
        
        use_case = ListCategory(repository=repository)
        input = ListCategoryInput()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output == ListCategoryOutput(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_activate=category.is_activate
                ) for category in repository.categories
            ]
        )
    
    def test_list_empty_categories(self):
        repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=repository)
        input = ListCategoryInput()
        output = use_case.execute(input)

        assert len(output.data) == 0
        assert output == ListCategoryOutput(data=[])
    