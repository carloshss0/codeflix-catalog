import uuid
import pytest
from rest_framework.test import APIClient

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


# Create your tests here.

@pytest.fixture
def cast_member_john():
    return CastMember(
        name="John Doe",
        type= CastMemberType.ACTOR,
    )

@pytest.fixture
def cast_member_marie():
    return CastMember(
        name="Marie Doe",
        type= CastMemberType.DIRECTOR,
    )

@pytest.fixture
def cast_member_repository():
    return DjangoORMCastMemberRepository()

@pytest.mark.django_db
class TestListAPI:

    def test_list_categories(
            self,
            cast_member_john: CastMember,
            cast_member_marie: CastMember,
            cast_member_repository: DjangoORMCastMemberRepository
        ):
        repository = cast_member_repository
        

        repository.save(cast_member_john)
        repository.save(cast_member_marie)


        url = '/api/cast_members/'
        response = APIClient().get(url)
        expected_data = {
            "data": [
            {
                "id": str(cast_member_john.id),
                "name": "John Doe",
                "type": "ACTOR",
            },
            {
                "id": str(cast_member_marie.id),
                "name": "Marie Doe",
                "type": "DIRECTOR",
            }
        ]}
        assert response.status_code == 200
        assert response.data == expected_data

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_retrieve_when_id_is_invalid(self) -> None:
        url = '/api/cast_members/invalid-id/'
        response = APIClient().get(url)
        assert response.status_code == 400
    
    def test_retrieve_cast_member_when_exists(self):
        repository = DjangoORMCastMemberRepository()

        cast_member = CastMember(
            name = "John Doe",
            type = CastMemberType.ACTOR
        )

        repository.save(cast_member)

        url = f'/api/cast_members/{cast_member.id}/'    

        response = APIClient().get(url)
        expected_data = {
            "data": {
                "id": str(cast_member.id),
                "name": "John Doe",
                "type": "ACTOR",
            }
        }
        assert response.status_code == 200
        assert response.data == expected_data

    def test_return_404_when_cast_member_not_exists(self) -> None:
        
        non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
        url = f'/api/cast_members/{non_existent_id}/'

        response = APIClient().get(url)

        print(response)

        assert response.status_code == 404
        # assert response.data == {"detail": "Not found."}

@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member_with_invalid_data(self):
        url = '/api/cast_members/'
        data = {
            "name": "John Doe",
            "type": "INVALID_TYPE"
        }
        response = APIClient().post(url, data)
        assert response.status_code == 400

    def test_create_cast_member_with_valid_data(self):
        url = '/api/cast_members/'
        data = {
            "name": "John Doe",
            "type": "ACTOR"
        }
        response = APIClient().post(url, data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_cast_member_with_invalid_data(
            self,
            cast_member_john,
            cast_member_repository
    ):
        cast_member_repository.save(cast_member_john)

        url = f"/api/cast_members/{str(cast_member_john.id)}/"

        data = {
            "name": "",
            "type": "DIRECTOR"
        }

        response = APIClient().put(url, data)
        assert response.status_code == 400

    def test_update_cast_member_with_non_existing_id(self):

        url = f"/api/cast_members/{str(uuid.uuid4())}/"

        data = {
            "name": "John Doe",
            "type": "DIRECTOR"
        }

        response = APIClient().put(url, data)
        assert response.status_code == 404

    def test_update_cast_member_with_valid_data(
            self,
            cast_member_john,
            cast_member_repository
    ):
        cast_member_repository.save(cast_member_john)

        url = f"/api/cast_members/{str(cast_member_john.id)}/"

        data = {
            "name": "John Doe Updated",
            "type": "DIRECTOR"
        }

        response = APIClient().put(url, data)
        assert response.status_code == 204


        
@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_cast_member_with_invalid_id(self):
        url = '/api/cast_members/invalid-id/'
        response = APIClient().delete(url)
        assert response.status_code == 400

    def test_delete_cast_member_when_exists(
            self,
            cast_member_john,
            cast_member_repository
    ):
        cast_member_repository.save(cast_member_john)

        url = f"/api/cast_members/{str(cast_member_john.id)}/"
        response = APIClient().delete(url)
        assert response.status_code == 204
    
    def test_delete_cast_member_with_non_existig_id(self):
        url = f"/api/cast_members/{str(uuid.uuid4())}/"
        response = APIClient().delete(url)
        assert response.status_code == 404
