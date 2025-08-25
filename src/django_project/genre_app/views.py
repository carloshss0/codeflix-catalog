from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from src.core.genre.application.update_genre import UpdateGenre, UpdateGenreInput
from src.core.genre.application.get_genre import GetGenre, GetGenreInput
from src.core.genre.application.delete_genre import DeleteGenre, DeleteGenreInput
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.create_genre import CreateGenre, CreateGenreInput
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.serializers import CreateGenreRequestSerializer, CreateGenreResponseSerializer, DeleteGenreRequestSerializer, ListGenreResponseSerializer, PatchGenreRequestSerializer, RetrieveGenreRequestSerializer, RetrieveGenreResponseSerializer, UpdateGenreRequestSerializer
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.core.genre.application.list_genre import ListGenre, ListGenreInput

# Create your views here.
class GenreViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        input = ListGenreInput()
        repository = DjangoORMGenreRepository()
        use_case = ListGenre(repository=repository)
        output = use_case.execute(input)

        serializer = ListGenreResponseSerializer(instance = output)

        return Response(
            status=HTTP_200_OK,
            data = serializer.data
        )
    
    def retrieve(self, request: Request, pk: str) -> Response:
        serializer = RetrieveGenreRequestSerializer(data={"id": pk})

        serializer.is_valid(raise_exception=True)

        
        repository = DjangoORMGenreRepository()
        use_case = GetGenre(repository=repository)
        input = GetGenreInput(id=serializer.validated_data["id"])

        try:
            output = use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        category_output = RetrieveGenreResponseSerializer(instance=output)
        
        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateGenreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        use_case = CreateGenre(repository=genre_repository, category_repository=category_repository)
        
        input = CreateGenreInput(
            name = serializer.validated_data["name"],
            is_active = serializer.validated_data["is_active"],
            categories = set(serializer.validated_data["categories"])
        )
        # input = CreateGenreInput(**serializer.validated_data)
        try:
            output = use_case.execute(input)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        category_ouput = CreateGenreResponseSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=category_ouput.data
        )

    def update(self, request: Request, pk: UUID = None) -> Response:

        serializer = UpdateGenreRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        input = UpdateGenreInput(
            id = serializer.validated_data["id"],
            name = serializer.validated_data["name"],
            is_active = serializer.validated_data["is_active"],
            categories = set(serializer.validated_data["categories"])
        )

        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    def partial_update(self, request: Request, pk: UUID = None) -> Response:
        serializer = PatchGenreRequestSerializer(data=
            {
                **request.data,
                "id": pk,
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        input = UpdateGenreInput(
            id = serializer.validated_data["id"],
            name = serializer.validated_data.get("name", None),
            is_active = serializer.validated_data.get("is_active", None),
            categories = set(serializer.validated_data["categories"]) if "categories" in serializer.validated_data else None
        )
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def destroy(self, request: Request, pk: UUID = None) -> Response:
        serializer = DeleteGenreRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMGenreRepository()
        use_case = DeleteGenre(repository=repository)
        input = DeleteGenreInput(id=serializer.validated_data["id"])
        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    
        


