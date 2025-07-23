from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK

from core.category.application.list_category import ListCategory, ListCategoryInput
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