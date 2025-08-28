import uuid
import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


@pytest.mark.django_db
class TestCastMemberRepository:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(
            name = "Action",
            type = CastMemberType.ACTOR
        )
        CastMemberORM.objects.count() == 0
        cast_member_repository = DjangoORMCastMemberRepository()

        cast_member_repository.save(cast_member)

        assert CastMemberORM.objects.count() == 1
        cast_member_model = CastMemberORM.objects.first()
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == str(cast_member.type)
    
    def test_get_cast_member_by_id(self):
        repository = DjangoORMCastMemberRepository()

        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        repository.save(cast_member)

        cast_member_fetched = repository.get_by_id(cast_member.id)

        assert cast_member_fetched is not None
        assert cast_member_fetched.id == cast_member.id
        assert cast_member_fetched.name == cast_member.name
        assert str(cast_member_fetched.type) == cast_member.type


    def test_get_cast_member_by_id_not_found(self):
        repository = DjangoORMCastMemberRepository()

        cast_member_fetched = repository.get_by_id(uuid.uuid4())

        assert cast_member_fetched is None

    
    def test_delete_cast_member_by_id(self):
        repository = DjangoORMCastMemberRepository()

        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1

        repository.delete(cast_member.id)
        assert CastMemberORM.objects.count() == 0

    
    def test_delete_cast_member_by_id_not_found(self):
        repository = DjangoORMCastMemberRepository()

        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1

        repository.delete(uuid.uuid4())
        assert CastMemberORM.objects.count() == 1

    
    def test_update_cast_member(self):
        repository = DjangoORMCastMemberRepository()

        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        repository.save(cast_member)

        cast_member.update_cast_member(
            name="John Doe Updated",
            type=CastMemberType.DIRECTOR)
        
        repository.update(cast_member)

        cast_member_model = CastMemberORM.objects.get(id=cast_member.id)
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == "John Doe Updated"
        assert cast_member_model.type == str(CastMemberType.DIRECTOR)


    def test_list_cast_member(self):

        repository = DjangoORMCastMemberRepository()

        cast_member_1 = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        cast_member_2 = CastMember(
            name = "Jane Doe",
            type = CastMemberType.DIRECTOR
        )

        repository.save(cast_member_1)
        repository.save(cast_member_2)

        cast_members = repository.list()
        assert len(cast_members) == 2
        assert cast_members[0].id == cast_member_1.id
        assert cast_members[1].id == cast_member_2.id 
        assert cast_members[0].name == cast_member_1.name
        assert cast_members[1].name == cast_member_2.name
        assert cast_members[0].type == cast_member_1.type
        assert cast_members[1].type == cast_member_2.type