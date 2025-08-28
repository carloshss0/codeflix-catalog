from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.create_cast_member import CreateCastMember, CreateCastMemberInput
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository



class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input = CreateCastMemberInput(
            name="John Doe",
            type=CastMemberType.DIRECTOR,

        )
        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert len(repository.cast_members) == 1
        assert repository.cast_members[0].id == output.id
        assert repository.cast_members[0].name == "John Doe"
        assert repository.cast_members[0].type == "DIRECTOR"

