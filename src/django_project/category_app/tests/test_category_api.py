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
        is_activate=True
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Series",
        description="Category for series",
        is_activate=True
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
        expected_data = [
            {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Category for movies",
                "is_activate": True,
            },
            {
                "id": str(category_documentary.id),
                "name": "Series",
                "description": "Category for series",
                "is_activate": True,
            }
        ]
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
            "id": str(category_movie.id),
            "name": "Movie",
            "description": "Category for movies",
            "is_activate": True,
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