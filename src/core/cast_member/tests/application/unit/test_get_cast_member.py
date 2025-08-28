from unittest.mock import MagicMock
import uuid
import pytest
from uuid import UUID


from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.get_cast_member import GetCastMember, GetCastMemberInput
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestGetCastMember:
    def test_get_cast_member_successfully(self):
        cast_member = CastMember(
            name="Test Category",
            type=CastMemberType.ACTOR,
        )
        
        mock_repository = MagicMock(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member
        use_case = GetCastMember(
            repository=mock_repository
        )
        input = GetCastMemberInput(
            id= cast_member.id,  # Assuming UUID is generated here for the test
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert mock_repository.get_by_id.called is True

    def test_get_cast_member_when_it_does_not_exist(self):
        mock_repository = MagicMock(CastMemberRepository)
        mock_repository.get_by_id.return_value = None
        use_case = GetCastMember(
            repository=mock_repository
        )

        input = GetCastMemberInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(CastMemberNotFound, match=f"Cast Member with id {input.id} not found."):
            use_case.execute(input)