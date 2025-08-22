from uuid import UUID

import pytest
from src.core.category.domain.category import Category
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.infrastructure.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.application.update_genre import UpdateGenre, UpdateGenreInput
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


class TestUpdateGenre:
    def test_update_genre_when_it_does_not_exist(self):

        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository
        )

        input_data = UpdateGenreInput(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="Updated Genre",
            categories=set(),
            is_active=True
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(input_data)

    
    def test_update_genre_with_invalid_name(
        self,
        movie_category,
        documentary_category
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])

        drama_genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(drama_genre)

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenreInput(
            id=drama_genre.id,
            name="",  # Invalid name
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input)

    def test_update_genre_with_invalid_categories(
            self,
            movie_category,
            documentary_category
    ):

        category_repository = InMemoryGenreRepository()
        category_repository.save(movie_category)

        genre_repository = InMemoryGenreRepository()

        drame_genre = Genre(
            name="Drama",
            categories={movie_category.id},
        )

        genre_repository.save(drame_genre)


        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository)

        input = UpdateGenreInput(
            id= drame_genre.id,
            name="Updated Genre",
            categories={movie_category.id, documentary_category.id},
            is_active=True
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)


    def test_update_genre_with_valid_data(
        self,
        movie_category,
        documentary_category
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])

        drama_genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(drama_genre)

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenreInput(
            id=drama_genre.id,
            name="Updated Drama",
            categories=set(),
            is_active=False
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(drama_genre.id)
        
        assert updated_genre.name == "Updated Drama"
        assert updated_genre.categories == set()
        assert not updated_genre.is_active