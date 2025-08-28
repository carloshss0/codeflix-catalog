from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMemberType



@dataclass
class UpdateCastMemberInput:
    id: UUID
    name: str | None = None
    type: CastMemberType | None = None
    

class UpdateCastMember:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, input: UpdateCastMemberInput) -> None:
        cast_member = self.repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFound(f"Cast Member with id {input.id} not found.")

        current_name = cast_member.name
        current_type = cast_member.type
    
        if input.name is not None:
            current_name = input.name

        if input.type is not None:
            current_type = input.type

        cast_member.update_cast_member(
            name=current_name,
            type=current_type,
        )

        self.repository.update(cast_member)