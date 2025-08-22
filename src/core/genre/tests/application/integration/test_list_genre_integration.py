from src.core.category.domain.category import Category
from src.core.category.infrastructure.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.list_genre import ListGenre, ListGenreInput
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.infrastructure.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenreUserCase:

    def test_list_genre_with_associated_categories(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")

        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        drama_genre = Genre(
                name= "Drama",
                categories= {movie_category.id, documentary_category.id}
            )
        genre_repository.save(drama_genre)

        fiction_genre = Genre(
                name= "Fiction",
                categories= {movie_category.id, documentary_category.id}
            )
        genre_repository.save(fiction_genre)

        use_case = ListGenre(repository = genre_repository)
        input = ListGenreInput()

        output = use_case.execute(input=input)
        
        assert len(output.data) == 2
        assert output.data[0].name == "Drama"
        assert output.data[1].name == "Fiction"
        assert output.data[0].categories == {movie_category.id, documentary_category.id}
        assert output.data[1].categories == {movie_category.id, documentary_category.id}

    
    def test_list_genre_when_no_genres_exist(self):
        genre_repository = InMemoryGenreRepository()
        use_case = ListGenre(repository=genre_repository)
        input = ListGenreInput()

        output = use_case.execute(input=input)

        assert len(output.data) == 0
        