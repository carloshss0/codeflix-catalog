import uuid

import pytest
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.get_cast_member import GetCastMember, GetCastMemberInput, GetCastMemberOutput
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestGetCastMember:
    def test_get_cast_member_by_id(self):
        john = CastMember(
            name = "John",
            type=CastMemberType.ACTOR,
        )

        marie = CastMember(
            name = "Marie",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(john)
        repository.save(marie)
        
        use_case = GetCastMember(repository=repository)
        
        input = GetCastMemberInput(
            id = john.id,
        )

        output = use_case.execute(input)

        assert output == GetCastMemberOutput(
            id=john.id,
            name="John",
            type="ACTOR",
        )

    def test_get_cast_member_when_it_does_not_exist(self):
        repository = InMemoryCastMemberRepository()
        use_case = GetCastMember(repository=repository)
        input = GetCastMemberInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(CastMemberNotFound, match=f"Cast Member with id {input.id} not found."):
            use_case.execute(input)