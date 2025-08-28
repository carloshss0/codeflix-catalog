
import pytest
from src.core.cast_member.application.update_category import UpdateCastMember, UpdateCastMemberInput
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infrastructure.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_can_update_cast_member_name_and_type(self):
        
        cast_member = CastMember(
                name = "John Doe",
                type= CastMemberType.DIRECTOR,
            )

        repository = InMemoryCastMemberRepository()

        repository.save(cast_member)
        use_case = UpdateCastMember(repository=repository)

        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="John Doe Updated",
            type=CastMemberType.ACTOR
        )

        use_case.execute(input)
        cast_member_from_repo = repository.get_by_id(cast_member.id)

        assert cast_member_from_repo.name == "John Doe Updated"
        assert cast_member_from_repo.type == CastMemberType.ACTOR
        assert len(repository.cast_members) == 1

    def test_cannot_update_with_invalid_data(self):
        cast_member = CastMember(
            name = "John Doe",
            type= CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)
        use_case = UpdateCastMember(repository=repository)

        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="",
            type=CastMemberType.ACTOR
        )

        with pytest.raises(ValueError, match="name cannot be empty"):
            use_case.execute(input)

        cast_member_from_repo = repository.get_by_id(cast_member.id)

        assert cast_member_from_repo.name == "John Doe"
        assert cast_member_from_repo.type == CastMemberType.DIRECTOR
        assert len(repository.cast_members) == 1