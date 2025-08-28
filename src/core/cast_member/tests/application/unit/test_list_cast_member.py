from unittest.mock import create_autospec

from src.core.cast_member.application.list_cast_member import CastMemberOutput, ListCastMember, ListCastMemberInput, ListCastMemberOutput
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
    def test_when_no_cast_member_in_repository(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = []
        use_case = ListCastMember(repository=mock_repository)
        input = ListCastMemberInput()
        output = use_case.execute(input = input)

        assert output == ListCastMemberOutput(data=[])
        assert mock_repository.list.called is True

    def test_when_cast_member_in_repository(self):
        mock_repository = create_autospec(CastMemberRepository)

        list_cast_member = [
            CastMember(
                name="John Doe",
                type=CastMemberType.ACTOR
            ),
            CastMember(
                name="Marie Johnson",
                type=CastMemberType.DIRECTOR
            )
        ]

        mock_repository.list.return_value = list_cast_member
        use_case = ListCastMember(repository=mock_repository)
        input = ListCastMemberInput()
        output = use_case.execute(input = input)

        assert output == ListCastMemberOutput(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                ) for cast_member in list_cast_member
            ]
        )

        assert mock_repository.list.called is True
        assert len(output.data) == 2