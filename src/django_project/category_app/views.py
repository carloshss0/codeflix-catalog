from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.get_category import GetCategory, GetCategoryInput
from src.core.category.application.list_category import ListCategory, ListCategoryInput
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel
# Create your views here.
class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
       input = ListCategoryInput()
       repository = DjangoORMCategoryRepository(CategoryModel)
       use_case = ListCategory(repository=repository)
       output = use_case.execute(input)

       categories = [
           {
               "id": str(category.id),
               "name": category.name,
               "description": category.description,
               "is_activate": category.is_activate
           } for category in output.data
       ]

       return Response(
           status=HTTP_200_OK,
           data = categories
       )
    
    def retrieve(self, request: Request, pk: str) -> Response:
        try:
            category_id = UUID(pk)

        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        repository = DjangoORMCategoryRepository()
        use_case = GetCategory(repository=repository)
        input = GetCategoryInput(id=category_id)

        try:
            output = use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_200_OK,
            data={
                "id": str(output.id),
                "name": output.name,
                "description": output.description,
                "is_activate": output.is_activate
            }
        )


