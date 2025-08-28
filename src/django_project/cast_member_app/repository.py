from uuid import UUID
from django.db import transaction
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel | None = None):
        self.cast_member_model = cast_member_model or CastMemberModel

    def save(self, cast_member: CastMemberModel) -> None:
        self.cast_member_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    def get_by_id(self, id: UUID) -> CastMemberModel | None:
        try:
            cast_member_model = self.cast_member_model.objects.get(id=id)
            return CastMember(
                id=cast_member_model.id,
                name=cast_member_model.name,
                type=CastMemberType(cast_member_model.type),
            )
        except self.cast_member_model.DoesNotExist:
            return None
    
    def delete(self, id: UUID) -> None:
        try:
            cast_member_model = self.cast_member_model.objects.get(id=id)
            cast_member_model.delete()
        except self.cast_member_model.DoesNotExist:
            pass
    
    def list(self) -> list[CastMember]:
        cast_members = self.cast_member_model.objects.all()
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType(cast_member.type),
            ) for cast_member in cast_members
        ]
    
    def update(self, cast_member: CastMember) -> None:
        try:
            cast_member_model_retrieved = self.cast_member_model.objects.get(id=cast_member.id)
        except cast_member_model_retrieved.DoesNotExist: ## smell bed.
            return None
        
        with transaction.atomic():
            self.cast_member_model.objects.filter(id=cast_member.id).update(
                name=cast_member.name,
                type=str(cast_member.type)
            )
        