import uuid
import pytest
from rest_framework.test import APIClient

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
# Create your tests here.

@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Category for movies",
        is_active=True
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Series",
        description="Category for series",
        is_active=True
    )

@pytest.fixture
def category_repository():
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListAPI:

    def test_list_categories(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository):
        repository = category_repository
        

        repository.save(category_movie)
        repository.save(category_documentary)


        url = '/api/categories/'
        response = APIClient().get(url)
        expected_data = {
            "data": [
            {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Category for movies",
                "is_active": True,
            },
            {
                "id": str(category_documentary.id),
                "name": "Series",
                "description": "Category for series",
                "is_active": True,
            }
        ]}
        assert response.status_code == 200
        assert response.data == expected_data

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_retrieve_when_id_is_invalid(self) -> None:
        url = '/api/categories/invalid-id/'
        response = APIClient().get(url)
        assert response.status_code == 400
    
    def test_retrieve_category_when_exists(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository
    ) -> None:
        repository = category_repository
        repository.save(category_movie)
        repository.save(category_documentary)

        url = f'/api/categories/{category_movie.id}/'    

        response = APIClient().get(url)
        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Category for movies",
                "is_active": True,
            }
        }
        assert response.status_code == 200
        assert response.data == expected_data

    def test_return_404_when_category_not_exists(self) -> None:
        
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
        url = f'/api/categories/{non_existent_id}/'

        response = APIClient().get(url)

        print(response)

        assert response.status_code == 404
        # assert response.data == {"detail": "Not found."}

@pytest.mark.django_db
class TestCreateAPI:
    def test_create_category_with_invalid_data(self):
        url = '/api/categories/'
        data = {
            "name": "",
            "description": "A category without a name",
            "is_active": True
        }
        response = APIClient().post(url, data)
        assert response.status_code == 400

    def test_create_category_with_valid_data(
            self,
            category_repository: DjangoORMCategoryRepository
        ):
        url = '/api/categories/'
        data = {
            "name": "New Category",
            "description": "A new category for testing",
            "is_active": True
        }
        response = APIClient().post(url, data)
        
        created_category_id = uuid.UUID(response.data.get("id"))

        created_category_repository = category_repository.get_by_id(created_category_id)
        assert created_category_repository is not None
        assert created_category_repository == Category(
            id=created_category_id,
            name="New Category",
            description="A new category for testing",
            is_active=True
        )

        
        assert response.status_code == 201

@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_category_with_invalid_data(self):
        url = '/api/categories/invalid-id/'
        data = {
            "name": "",
            "description": "An updated category without a name",
            "is_active": True
        }
        response = APIClient().put(url, data)
        assert response.status_code == 400

    def test_update_category_with_valid_data(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        data = {
            "id": str(category_movie.id),
            "name": "Updated Category",
            "description": "An updated category for testing",
            "is_active": True
        }
        response = APIClient().put(url, data)
        assert response.status_code == 204

        
        updated_category_repository = repository.get_by_id(category_movie.id)
        
        assert updated_category_repository is not None
        assert updated_category_repository == Category(
            id=category_movie.id,
            name="Updated Category",
            description="An updated category for testing",
            is_active=True
        )

        

    def test_update_non_existent_category(self):
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
        url = f'/api/categories/{non_existent_id}/'
        
        data = {
            "id": non_existent_id,
            "name": "Non Existent Category",
            "description": "This category does not exist",
            "is_active": True
        }
        
        response = APIClient().put(url, data)
        
        assert response.status_code == 404

@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_category_with_invalid_id(self):
        url = '/api/categories/invalid-id/'
        response = APIClient().delete(url)
        assert response.status_code == 400

    def test_delete_category_when_exists(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().delete(url)
        
        assert response.status_code == 204
        
        deleted_category_repository = repository.get_by_id(category_movie.id)
        assert deleted_category_repository is None

    def test_delete_non_existent_category(self):
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
        url = f'/api/categories/{non_existent_id}/'
        
        response = APIClient().delete(url)
        
        assert response.status_code == 404

@pytest.mark.django_db
class TestPartialAPI:
    def test_partial_update_category_with_invalid_data(self):
        url = '/api/categories/invalid-id/'
        data = {
            "name": "random name",
        }
        response = APIClient().patch(url, data)
        assert response.status_code == 400

    def test_partial_update_category_name(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        data = {
            "name": "Partially Updated Category"
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 204
        
        updated_category_repository = repository.get_by_id(category_movie.id)
        
        assert updated_category_repository is not None
        assert updated_category_repository.name == "Partially Updated Category"


    def test_partial_update_category_description(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        data = {
            "description": "Partially Updated Description"
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 204
        
        updated_category_repository = repository.get_by_id(category_movie.id)
        
        assert updated_category_repository is not None
        assert updated_category_repository.description == "Partially Updated Description"

    def test_partial_update_category_is_active(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ):
        repository = category_repository
        repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        data = {
            "is_active": False
        }
        response = APIClient().patch(url, data)
        
        assert response.status_code == 204
        
        updated_category_repository = repository.get_by_id(category_movie.id)
        
        assert updated_category_repository is not None
        assert updated_category_repository.is_active is False

    
    def test_partial_update_non_existent_category(self):
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
        url = f'/api/categories/{non_existent_id}/'
        
        data = {
            "name": "Non Existent Category",
        }
        
        response = APIClient().patch(url, data)
        
        assert response.status_code == 404