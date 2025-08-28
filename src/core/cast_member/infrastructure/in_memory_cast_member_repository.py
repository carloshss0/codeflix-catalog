from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository



class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members=None):
        self.cast_members = cast_members or []

    def save(self, cast_member) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> CastMember:
        for cast_member in self.cast_members:
            if cast_member.id == id:
                return cast_member
        return None

    def delete(self, id: UUID) -> None:
        for cast_member in self.cast_members:
            if cast_member.id == id:
                self.cast_members.remove(cast_member)
                return
        return None
    
    def update(self, cast_member: CastMember) -> None:
        old_cast_member = self.get_by_id(cast_member.id)
        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)

    def list(self) -> list[CastMember]:
        return self.cast_members
        
    
