from unittest.mock import MagicMock
import pytest
from uuid import UUID

from src.core.cast_member.application.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.create_cast_member import CreateCastMember, CreateCastMemberInput
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        mock_repository = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(
            repository=mock_repository
        )
        input = CreateCastMemberInput(
            name="John Doe",
            type=CastMemberType.ACTOR
        )

        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert mock_repository.save.called is True

    def test_create_cast_member_with_invalid_data(self):
        mock_repository = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(
            repository=mock_repository
        )
        with pytest.raises(InvalidCastMemberData):
            use_case.execute(
                CreateCastMemberInput(
                    name="",  # Invalid name
                    type=CastMemberType.DIRECTOR
                )
            )