import pytest
from uuid import UUID
import uuid
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match= "missing 1 required positional argument: 'name'"):
            CastMember(type= CastMemberType.DIRECTOR)
    def test_empty_name_must_raise_an_exception(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name= "", type= CastMemberType.DIRECTOR)

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match= "name must have less than 256 characters"):
            CastMember("a"*256, type= CastMemberType.DIRECTOR)

    def test_cast_member_must_be_created_with_id_as_uuid(self):
        category = CastMember(name= "John Doe", type= CastMemberType.DIRECTOR)
        assert isinstance(category.id, UUID)

    def test_cast_member_raise_exception_when_type_is_invalid(self):
        with pytest.raises(ValueError, match= "type must be either 'DIRECTOR' or 'ACTOR'"):
            CastMember(name= "John Doe", type= "WRITER")

    def test_cast_member_raise_exception_when_type_is_not_passed(self):
        with pytest.raises(TypeError, match= "missing 1 required positional argument: 'type'"):
            CastMember(name= "John Doe")

    def test_cast_member_raise_exception_when_type_is_empty(self):
        with pytest.raises(ValueError, match= "type must be either 'DIRECTOR' or 'ACTOR'"):
            CastMember(name= "John Doe", type= "")

    def test_cast_member_is_created_with_provided_values(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="John Doe",
            type=CastMemberType.DIRECTOR     
        )
        assert cast_member.id == cast_member_id
        assert cast_member.name == "John Doe"
        assert cast_member.type == "DIRECTOR"
    

    def test_str_method_for_cast_member(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        string_str = f"{cast_member.id} - {cast_member.name} - {cast_member.type}"
        assert str(cast_member) == string_str

    def test_repr_method_for_category(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        string_str = f"<Cast Member {cast_member.id} - {cast_member.name} - {cast_member.type}"
        assert repr(cast_member) == string_str



class TestEqualCastMember:
    def test_when_cast_member_have_same_id_they_are_equal(self):
        cast_member_id = uuid.uuid4()
        cast_member_1 = CastMember(name= "Marie Doe", id= cast_member_id, type= CastMemberType.DIRECTOR)
        cast_member_2 = CastMember(name= "Marie Doe", id= cast_member_id, type= CastMemberType.DIRECTOR)

        assert cast_member_1 == cast_member_2

    def test_equality_different_classes(self):
        
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category_1 = CastMember(name= "Marie Doe", id= common_id, type= CastMemberType.DIRECTOR)

        dummy = Dummy()
        dummy.id = common_id

        assert category_1 != dummy