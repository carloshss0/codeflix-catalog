import pytest
from uuid import UUID
import uuid
from src.core.genre.domain.genre import Genre

class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match= "missing 1 required positional argument: 'name'"):
            Genre()
    def test_empty_name_must_raise_an_exception(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name= "")

    def test_non_boolean_is_active_must_raise_an_exception(self):
        with pytest.raises(ValueError, match="is_active must be a boolean value"):
            Genre(name="Action", is_active="yes")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match= "name must have less than 256 characters"):
            Genre("a"*256)

    def test_genre_must_be_created_with_id_as_uuid(self):
        genre = Genre(name="Action")
        assert isinstance(genre.id, UUID)


    def test_create_genre_without_optional_fields(self):
        genre = Genre(name="Commedy")
        assert genre.name == "Commedy"
        assert genre.is_active is True


    def test_genre_is_created_as_active_by_default(self):
        genre = Genre(name="Commedy")
        assert genre.is_active is True
    
    def test_genre_is_created_with_provided_values(self):
        genre_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre = Genre(
            id=genre_id,
            name="Comedy",
            is_active=False,
            categories={category_id}
        )
        assert genre.id == genre_id
        assert genre.name == "Comedy"
        assert genre.is_active is False
        assert category_id in genre.categories

    def test_str_method_for_genre(self):
        genre_id = uuid.uuid4()
        genre = Genre(
            id=genre_id,
            name="Comedy",
            is_active=False     
        )

        string_str = f"{genre.id} - {genre.name} - {genre.is_active}"
        assert str(genre) == string_str

    def test_repr_method_for_genre(self):
        genre_id = uuid.uuid4()
        genre = Genre(
            id=genre_id,
            name="Comedy",
            is_active=False     
        )

        string_str = f"<Genre {genre.id} - {genre.name} - {genre.is_active}"
        assert repr(genre) == string_str


class TestUpdateGenre:
    def test_update_category_with_name_and_description(self):
        genre = Genre(name="Commedy")
        genre.change_name(name="Drama")

        assert genre.name == "Drama"

    def test_update_category_with_invalid_name_must_raise_exception(self):
        genre = Genre(name="Commedy")
        with pytest.raises(ValueError, match= "name must have less than 256 characters"):
            genre.change_name(name= "a"*256)

    def test_cannot_update_category_with_empty_name(self):
        genre = Genre(name="Commedy")
        with pytest.raises(ValueError, match= "name cannot be empty"):
            genre.change_name(name= "")


class TestActivateGenre:
    def test_activate_category(self):
        genre = Genre(name="Drama", is_active=False)
        genre.activate()
        assert genre.is_active is True

    def test_deactivate_category(self):
        genre = Genre(name="Drama", is_active=True)
        genre.deactivate()
        assert genre.is_active is False


class TestEqualCategory:
    def test_when_categories_have_same_id_they_are_equal(self):
        genre_id = uuid.uuid4()
        genre_1 = Genre(name= "Drama", id= genre_id)
        genre_2 = Genre(name= "Drama", id= genre_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre_1 = Genre(name= "Drama", id= common_id)

        dummy = Dummy()
        dummy.id = common_id

        assert genre_1 != dummy