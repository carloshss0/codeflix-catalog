

from core.cast_member.application.list_cast_member import CastMemberOutput, ListCastMember, ListCastMemberInput, ListCastMemberOutput
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_list_cast_members(self):
        cast_member_1 = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        cast_member_2 = CastMember(
            name="Marie Johnson",
            type=CastMemberType.DIRECTOR
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member_1)
        repository.save(cast_member_2)
        
        use_case = ListCastMember(repository=repository)
        input = ListCastMemberInput()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output == ListCastMemberOutput(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                ) for cast_member in repository.cast_members
            ]
        )
    
    def test_list_empty_cast_members(self):
        repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=repository)
        input = ListCastMemberInput()
        output = use_case.execute(input)

        assert len(output.data) == 0
        assert output == ListCastMemberOutput(data=[])
    