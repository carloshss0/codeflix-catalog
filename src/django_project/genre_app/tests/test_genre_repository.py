import uuid
import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreORM

@pytest.mark.django_db
class TestGenreRepository:
    def test_saves_genre_in_database(self):
        genre = Genre(
            name = "Action",
        )
        GenreORM.objects.count() == 0
        genre_repository = DjangoORMGenreRepository()

        genre_repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
    
    def test_saves_genre_with_categories_in_database(self):

        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        movie_category = Category(
            name="Movie",
            description="Category for movies",
            is_active=True
        )

        documentary_category = Category(
            name="Documentary",
            description="Category for documentaries",
            is_active=True
        )

        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        assert GenreORM.objects.count() == 0
        genre = Genre(
            name = "Action",
            categories = {movie_category.id, documentary_category.id}
        )

        repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
        assert genre_model.categories.count() == 2

    def test_get_genre_by_id(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        movie_category = Category(
            name="Movie",
        )

        category_repository.save(movie_category)

        genre = Genre(
            name = "Action",
            categories = {movie_category.id}
        )

        repository.save(genre)

        genre_fetched = repository.get_by_id(genre.id)

        assert genre_fetched is not None
        assert genre_fetched.id == genre.id
        assert genre_fetched.name == genre.name
        assert genre_fetched.is_active == genre.is_active
        assert genre_fetched.categories == {movie_category.id}

    def test_get_genre_by_id_not_found(self):
        repository = DjangoORMGenreRepository()

        genre_fetched = repository.get_by_id(uuid.uuid4())

        assert genre_fetched is None

    
    def test_delete_genre_by_id(self):
        repository = DjangoORMGenreRepository()


        genre = Genre(
            name = "Action",
        )

        repository.save(genre)
        assert GenreORM.objects.count() == 1

        repository.delete(genre.id)
        assert GenreORM.objects.count() == 0

    
    def test_delete_genre_by_id_not_found(self):
        repository = DjangoORMGenreRepository()

        genre = Genre(
            name = "Action",
        )

        repository.save(genre)
        assert GenreORM.objects.count() == 1

        repository.delete(uuid.uuid4())
        assert GenreORM.objects.count() == 1

    
    def test_update_genre(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        movie_category = Category(
            name="Movie",
        )

        category_repository.save(movie_category)

        genre = Genre(
            name = "Action",
        )

        repository.save(genre)

        genre.change_name("Action Updated")
        genre.is_active = False
        genre.add_category(movie_category.id)
        repository.update(genre)

        genre_model = GenreORM.objects.get(id=genre.id)
        assert genre_model.id == genre.id
        assert genre_model.name == "Action Updated"
        assert genre_model.is_active == False
        assert genre_model.categories.count() == 1
        assert genre_model.categories.first().id == movie_category.id

    def test_list_genres(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        movie_category = Category(
            name="Movie",
        )

        documentary_category = Category(
            name="Documentary",
        )

        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre1 = Genre(
            name = "Action",
            categories = {movie_category.id}
        )

        genre2 = Genre(
            name = "Drama",
            is_active=False,
            categories = {documentary_category.id}
        )

        repository.save(genre1)
        repository.save(genre2)

        genres = repository.list()
        assert len(genres) == 2

        assert genres[0].id == genre1.id
        assert genres[0].name == genre1.name
        assert genres[0].is_active == genre1.is_active
        assert genres[0].categories == {movie_category.id}

        assert genres[1].id == genre2.id
        assert genres[1].name == genre2.name
        assert genres[1].is_active == genre2.is_active
        assert genres[1].categories == {documentary_category.id}