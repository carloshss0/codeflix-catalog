
import uuid
import pytest
from rest_framework.test import APIClient
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository

@pytest.fixture
def movie_category():
    return Category(
        name="Movie",
        description="Category for movies",
        is_active=True
    )

@pytest.fixture
def documentary_category():
    return Category(
        name="Documentary",
        description="Category for documentaries",
        is_active=True
    )

@pytest.fixture
def category_repository():

    category_repo = DjangoORMCategoryRepository()

    return category_repo

@pytest.fixture
def action_genre(movie_category, documentary_category):
    action_genre = Genre(
        name="Action",
        categories={movie_category.id, documentary_category.id}
    )

    return action_genre

@pytest.fixture
def commedy_genre(movie_category):
    commedy_genre = Genre(
        name="Commedy",
        categories={movie_category.id}
    )

    return commedy_genre


@pytest.fixture
def genre_repository():
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestViews:
    def test_list_genres(
            self,
            action_genre: Genre,
            commedy_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            genre_repository: DjangoORMGenreRepository,
            category_repository: DjangoORMCategoryRepository):
        
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)
        repository.save(commedy_genre)

        url = '/api/genres/'
        response = APIClient().get(url)

        assert response.status_code == 200
        assert response.data["data"][0]["id"] == str(action_genre.id)
        assert response.data["data"][0]["name"] == action_genre.name
        assert response.data["data"][0]["is_active"] == action_genre.is_active
        assert set(response.data["data"][0]["categories"]) == {str(movie_category.id), str(documentary_category.id)}

        assert response.data["data"][1]["id"] == str(commedy_genre.id)
        assert response.data["data"][1]["name"] == commedy_genre.name
        assert response.data["data"][1]["is_active"] == commedy_genre.is_active
        assert set(response.data["data"][1]["categories"]) == {str(movie_category.id)}


@pytest.mark.django_db
class TestCreateGenre:
    def test_create_genre(
            self,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        url = '/api/genres/'
        data = {
            "name": "Horror",
            "categories": [str(movie_category.id), str(documentary_category.id)],
            "is_active": True
        }
        response = APIClient().post(url, data)
        assert response.status_code == 201

    def test_create_genre_with_invalid_category(
            self,
            movie_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        invalid_uuid = uuid.uuid4()
        url = '/api/genres/'
        data = {
            "name": "Horror",
            "categories": [str(movie_category.id), str(invalid_uuid)],
            "is_active": True
        }
        response = APIClient().post(url, data)
        assert response.status_code == 400
        assert str(invalid_uuid) in response.data["error"]

    def test_create_genre_with_no_category(
            self,
            genre_repository: DjangoORMGenreRepository
    ):
        url = '/api/genres/'
        data = {
            "name": "Horror",
            "categories": [],
            "is_active": True
        }
        response = APIClient().post(url, data)
        assert response.status_code == 201
        assert response.data["id"] is not None

    def test_create_genre_with_invalid_data(
            self,
            genre_repository: DjangoORMGenreRepository
    ):
        url = '/api/genres/'
        data = {
            "name": "",
            "categories": [],
            "is_active": "not-a-boolean"
        }
        response = APIClient().post(url, data)
        assert response.status_code == 400

@pytest.mark.django_db
class TestDeleteGenre:
    def test_delete_genre_by_id(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            genre_repository: DjangoORMGenreRepository,
            category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre_repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        response = APIClient().delete(url)
        assert response.status_code == 204
        assert genre_repository.get_by_id(action_genre.id) is None

    def test_delete_genre_with_invalid_id(
            self,
            genre_repository: DjangoORMGenreRepository
    ):
        invalid_uuid = uuid.uuid4()
        url = f'/api/genres/{invalid_uuid}/'
        response = APIClient().delete(url)
        assert response.status_code == 404

    def test_delete_genre_with_nonexistent_id(
            self,
            genre_repository: DjangoORMGenreRepository
    ):
        nonexistent_uuid = uuid.uuid4()
        url = f'/api/genres/{nonexistent_uuid}/'
        response = APIClient().delete(url)
        assert response.status_code == 404

@pytest.mark.django_db
class TestGet:
    def test_get_genre_by_id(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            genre_repository: DjangoORMGenreRepository,
            category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre_repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        response = APIClient().get(url)
        assert response.status_code == 200
        assert response.data["data"]["id"] == str(action_genre.id)
        assert response.data["data"]["name"] == action_genre.name
        assert response.data["data"]["is_active"] == action_genre.is_active
        assert set(response.data["data"]["categories"]) == {str(movie_category.id), str(documentary_category.id)}

    def test_get_genre_with_invalid_id(
            self,
            genre_repository: DjangoORMGenreRepository
    ):
        invalid_uuid = uuid.uuid4()
        url = f'/api/genres/{invalid_uuid}/'
        response = APIClient().get(url)
        assert response.status_code == 404

@pytest.mark.django_db
class TestUpdate:

    def test_when_request_data_is_valid_then_update_genre(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        data = {
            "name": "Updated Genre",
            "categories": [str(movie_category.id)],
            "is_active": False
        }
        response = APIClient().put(url, data)
        
        assert response.status_code == 204
        
        updated_genre = repository.get_by_id(action_genre.id)
        
        assert updated_genre is not None
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {movie_category.id}


    def test_when_request_data_is_invalid_then_return_400(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        data = {
            "name": "",
            "categories": ["not-a-uuid"],
            "is_active": "not-a-boolean"
        }
        response = APIClient().put(url, data)
        
        assert response.status_code == 400

    def test_when_related_categories_do_not_exist_then_return_400(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        invalid_uuid = uuid.uuid4()
        url = f'/api/genres/{action_genre.id}/'
        data = {
            "name": "Updated Genre",
            "categories": [str(invalid_uuid)],
            "is_active": True
        }
        response = APIClient().put(url, data)
        
        assert response.status_code == 400
        assert str(invalid_uuid) in response.data["error"]
    
    def test_when_genre_does_not_exist_then_return_404(
            self,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)


        nonexistent_uuid = uuid.uuid4()
        url = f'/api/genres/{nonexistent_uuid}/'
        data = {
            "name": "Updated Genre",
            "categories": [str(movie_category.id)],
            "is_active": True
        }
        response = APIClient().put(url, data)
        
        assert response.status_code == 404

@pytest.mark.django_db
class TestPartialUpdate:
    def test_when_request_data_is_valid_then_partial_update_genre(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        data = {
            "id": str(action_genre.id),
            "name": "Partially Updated Genre",
        }

        response = APIClient().patch(url, data)
        assert response.status_code == 204
        updated_genre = repository.get_by_id(action_genre.id)
        assert updated_genre is not None
        assert updated_genre.name == "Partially Updated Genre"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {movie_category.id, documentary_category.id}

    def test_when_request_data_is_invalid_then_return_400(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        url = f'/api/genres/{action_genre.id}/'
        data = {
            "id": str(action_genre.id),
            "name": "",
            "categories": ["not-a-uuid"],
            "is_active": "not-a-boolean"
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 400


    def test_when_related_categories_do_not_exist_then_return_400(
            self,
            action_genre: Genre,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_repository: DjangoORMGenreRepository
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        repository = genre_repository
        repository.save(action_genre)

        invalid_uuid = uuid.uuid4()
        url = f'/api/genres/{action_genre.id}/'
        data = {
            "id": str(action_genre.id),
            "categories": [str(invalid_uuid)],
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 400
        assert str(invalid_uuid) in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(
            self,
            movie_category: Category,
            documentary_category: Category,
            category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(movie_category)
        category_repository.save(documentary_category)


        nonexistent_uuid = uuid.uuid4()
        url = f'/api/genres/{nonexistent_uuid}/'
        data = {
            "id": str(nonexistent_uuid),
            "name": "Partially Updated Genre",
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 404


        