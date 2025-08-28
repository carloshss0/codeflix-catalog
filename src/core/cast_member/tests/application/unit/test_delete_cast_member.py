from unittest.mock import create_autospec
from uuid import UUID
import uuid
import pytest

from src.core.cast_member.application.delete_cast_member import DeleteCastMember, DeleteCastMemberInput
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType



class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        usecase = DeleteCastMember(repository=mock_repository)
        usecase.execute(DeleteCastMemberInput(cast_member.id))
        mock_repository.delete.assert_called_once_with(cast_member.id)

    def test_delete_cast_member_with_invalid_id(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None
        use_case = DeleteCastMember(
            repository=mock_repository
        )

        input = DeleteCastMemberInput(
            id=uuid.uuid4(),  # Invalid UUID for the test
        )
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input)
        
        mock_repository.get_by_id.assert_called_once_with(input.id)
        assert mock_repository.delete.called is False
