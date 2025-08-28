from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

@dataclass
class DeleteCastMemberInput:
    id: UUID


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
    
    def execute(self, input: DeleteCastMemberInput) -> None:
        category = self.repository.get_by_id(input.id)
        if not category:
            raise CastMemberNotFound(f"Cast Member with id {input.id} not found.")
        
        self.repository.delete(category.id)

 