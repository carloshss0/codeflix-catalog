from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

@dataclass
class CreateCastMemberInput:
    name: str
    type: CastMemberType ## Need to check

@dataclass
class CreateCastMemberOutput:
    id: UUID


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
    
    def execute(self, input: CreateCastMemberInput) -> CreateCastMemberOutput:
        try:
            cast_member = CastMember(
                name=input.name,
                type=input.type
            )
        except ValueError as err:
            raise InvalidCastMemberData(f"Invalid cast member data: {err}")

        self.repository.save(cast_member)
        return CreateCastMemberOutput(id=cast_member.id)