import uuid

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository



class TestMemoryCastMemberRepository:
    def test_can_save_category(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository.save(cast_member)
        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member
    
    def test_can_get_cast_member_by_id(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        retrieved_cast_member = repository.get_by_id(cast_member.id)
        assert retrieved_cast_member == cast_member
    
    def test_get_cast_member_by_id_returns_none_if_not_found(self):
        repository = InMemoryCastMemberRepository()
        cast_member_id = uuid.uuid4()
        retrieved_cast_member = repository.get_by_id(cast_member_id)

        assert retrieved_cast_member is None

    def test_can_delete_cast_member_by_id(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        repository.delete(cast_member.id)
        assert len(repository.cast_members) == 0

    def test_delete_cast_member_by_id_does_nothing_if_not_found(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        non_existent_id = uuid.uuid4()
        repository.delete(non_existent_id)
        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member

    def test_can_update_cast_member(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        updated_cast_member = CastMember(
            id=cast_member.id,
            name="John Doe Updated",
            type= CastMemberType.DIRECTOR
        )
        repository.update(updated_cast_member)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == updated_cast_member

    def test_update_cast_member_does_nothing_if_not_found(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        non_existent_cast_member = CastMember(
            id=uuid.uuid4(),
            name="Mock Joe",
            type=CastMemberType.DIRECTOR
        )
        repository.update(non_existent_cast_member)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member

    def test_can_list_cast_members(self):
        cast_member_1 = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        cast_member_2 = CastMember(
            name="Marie Doe",
            type=CastMemberType.DIRECTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member_1, cast_member_2])

        cast_members = repository.list()
        assert len(cast_members) == 2
        assert cast_members[0] == cast_member_1
        assert cast_members[1] == cast_member_2