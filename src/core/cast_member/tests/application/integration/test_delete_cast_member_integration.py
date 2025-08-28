from uuid import UUID
import uuid

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.delete_cast_member import DeleteCastMember, DeleteCastMemberInput
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository



class TestDeleteCastMember:
    def test_delete_cast_member_by_id(self):
        john = CastMember(
            name = "Movie",
            type=CastMemberType.ACTOR,
        )

        marie = CastMember(
            name = "Marie",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(john)
        repository.save(marie)
        use_case = DeleteCastMember(repository=repository)
        
        input = DeleteCastMemberInput(
            id = john.id,
        )
        assert repository.get_by_id(input.id) == john
        use_case.execute(input)

        assert repository.get_by_id(input.id) is None

    def test_delete_category_when_it_does_not_exist(self):

        repository = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(repository=repository)
        input = DeleteCastMemberInput(
            id = uuid.uuid4(),
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input)
        
        assert repository.get_by_id(input.id) is None


        
