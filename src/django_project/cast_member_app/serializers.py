from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType

class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # We use DRF's "choices," which allows a limited set of options for a given field.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Value coming from the API as a string is converted to the StrEnum
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        # The value coming from our domain is converted to a string for the API
        return str(super().to_representation(value))

class CastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()
    

class ListCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(many=True)

class RetrieveCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(source='*')

class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()

class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()

class DeleteCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()