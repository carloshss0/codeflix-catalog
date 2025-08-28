from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMemberType


@dataclass
class GetCastMemberInput:
    id: UUID

@dataclass
class GetCastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class GetCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
    
    def execute(self, input: GetCastMemberInput) -> GetCastMemberOutput:
        cast_member = self.repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFound(f"Cast Member with id {input.id} not found.")
        
        return GetCastMemberOutput(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type
        )