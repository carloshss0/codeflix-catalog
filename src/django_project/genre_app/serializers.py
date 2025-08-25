from rest_framework import serializers


class GenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(
        child=serializers.UUIDField(),
    )

class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(many=True)

class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(
        child=serializers.UUIDField(),
    )

class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(source='*')

class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(required=False)
    categories = serializers.ListField(
        child=serializers.UUIDField(),
    )

class PatchGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField(required=False)
    categories = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )