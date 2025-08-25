from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from src.core.category.application.delete_category import DeleteCategory, DeleteCategoryInput
from src.core.category.application.update_category import UpdateCategory, UpdateCategoryInput
from src.core.category.application.create_category import CreateCategory, CreateCategoryInput
from src.django_project.category_app.serializers import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, PatchCategoryRequestSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.get_category import GetCategory, GetCategoryInput
from src.core.category.application.list_category import ListCategory, ListCategoryInput
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
# Create your views here.
class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        input = ListCategoryInput()
        repository = DjangoORMCategoryRepository(CategoryModel)
        use_case = ListCategory(repository=repository)
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance = output)

        return Response(
            status=HTTP_200_OK,
            data = serializer.data
        )
    
    def retrieve(self, request: Request, pk: str) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})

        serializer.is_valid(raise_exception=True)

        
        repository = DjangoORMCategoryRepository()
        use_case = GetCategory(repository=repository)
        input = GetCategoryInput(id=serializer.validated_data["id"])

        try:
            output = use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        category_output = RetrieveCategoryResponseSerializer(instance=output)
        
        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCategoryRepository()
        use_case = CreateCategory(repository=repository)
        input = CreateCategoryInput(**serializer.validated_data)

        output = use_case.execute(input)

        category_ouput = CreateCategoryResponseSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=category_ouput.data
        )

    def update(self, request: Request, pk: UUID = None) -> Response:

        serializer = UpdateCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCategoryRepository()
        use_case = UpdateCategory(repository=repository)
        input = UpdateCategoryInput(**serializer.validated_data)

        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    def partial_update(self, request: Request, pk: UUID = None) -> Response:
        serializer = PatchCategoryRequestSerializer(data={
            **request.data,
            "id": pk,
        })

        serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = UpdateCategory(repository=repository)
        input = UpdateCategoryInput(**serializer.validated_data)
        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_204_NO_CONTENT
        )

    def destroy(self, request: Request, pk: UUID = None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCategoryRepository()
        use_case = DeleteCategory(repository=repository)
        input = DeleteCategoryInput(id=serializer.validated_data["id"])
        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    
        


