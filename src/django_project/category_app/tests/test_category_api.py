from uuid import UUID
from django.test import TestCase
from rest_framework.test import APITestCase

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel
# Create your tests here.
class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        repository = DjangoORMCategoryRepository(CategoryModel)
        category_movie = Category(
            name="Movie",
            description="Category for movies",
            is_activate=True
        )

        category_documentary = Category(
            name="Series",
            description="Category for series",
            is_activate=True
        )

        repository.save(category_movie)
        repository.save(category_documentary)


        url = '/api/categories/'
        response = self.client.get(url)
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
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, expected_data)