from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.update_category import UpdateCastMember, UpdateCastMemberInput
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCategory:
    def test_update_cast_member_name(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )
        
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository = mock_repository)
        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="John Doe Updated",
            type=CastMemberType.ACTOR
        )
        
        use_case.execute(input)
        assert cast_member.name == "John Doe Updated"
        assert cast_member.type == CastMemberType.ACTOR
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_that_does_not_exist_must_raise_an_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        non_existing_id = uuid.uuid4()
        use_case = UpdateCastMember(repository = mock_repository)
        input = UpdateCastMemberInput(
            id= non_existing_id,
            name="John Doe Updated",
            type=CastMemberType.ACTOR
        )
        
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input)
        
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_not_called()


    def test_update_cast_member_with_invalid_data(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )
        
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository = mock_repository)
        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="John Smith",
            type="WRITER"  # Invalid type
        )
        
        with pytest.raises(ValueError) as exc_info:
            use_case.execute(input)
        
        assert str(exc_info.value) == "type must be either 'DIRECTOR' or 'ACTOR'"
        assert mock_repository.get_by_id.called is True
        mock_repository.update.assert_not_called()






