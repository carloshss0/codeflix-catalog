from django.shortcuts import render
from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)

from src.core.cast_member.application.delete_cast_member import DeleteCastMember, DeleteCastMemberInput
from src.core.cast_member.application.update_category import UpdateCastMember, UpdateCastMemberInput
from src.core.cast_member.application.create_cast_member import CreateCastMember, CreateCastMemberInput
from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMemberData
from src.core.cast_member.application.get_cast_member import GetCastMember, GetCastMemberInput
from src.django_project.cast_member_app.serializers import CreateCastMemberRequestSerializer, CreateCastMemberResponseSerializer, DeleteCastMemberRequestSerializer, ListCastMemberResponseSerializer, RetrieveCastMemberRequestSerializer, RetrieveCastMemberResponseSerializer, UpdateCastMemberRequestSerializer
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.core.cast_member.application.list_cast_member import ListCastMember, ListCastMemberInput

# Create your views here.
class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCastMemberInput()
        repository = DjangoORMCastMemberRepository()
        use_case = ListCastMember(repository=repository)
        output = use_case.execute(input)

        serializer = ListCastMemberResponseSerializer(instance = output)

        return Response(
            status=HTTP_200_OK,
            data = serializer.data
        )
    
    def retrieve(self, request: Request, pk: str) -> Response:
        serializer = RetrieveCastMemberRequestSerializer(data={"id": pk})

        serializer.is_valid(raise_exception=True)

        
        repository = DjangoORMCastMemberRepository()
        use_case = GetCastMember(repository=repository)
        input = GetCastMemberInput(id=serializer.validated_data["id"])

        try:
            output = use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        category_output = RetrieveCastMemberResponseSerializer(instance=output)
        
        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input = CreateCastMemberInput(**serializer.validated_data)

        output = use_case.execute(input)

        category_ouput = CreateCastMemberResponseSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=category_ouput.data
        )

    def update(self, request: Request, pk: UUID = None) -> Response:

        serializer = UpdateCastMemberRequestSerializer(data={
            **request.data,
            "id": pk,
        })
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCastMemberRepository()
        use_case = UpdateCastMember(repository=repository)
        input = UpdateCastMemberInput(**serializer.validated_data)

        try:
            use_case.execute(input)

        except InvalidCastMemberData as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    def destroy(self, request: Request, pk: UUID = None) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        repository = DjangoORMCastMemberRepository()
        use_case = DeleteCastMember(repository=repository)
        input = DeleteCastMemberInput(id=serializer.validated_data["id"])
        try:
            use_case.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    

    ## There was not a requirement for a PATCH API Endpoint for the Cast Member domain.
