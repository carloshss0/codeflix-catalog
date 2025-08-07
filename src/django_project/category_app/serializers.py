from rest_framework import serializers

class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField()

class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)

class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source='*')

class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField()

class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=False)

class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class PatchCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=False)
    