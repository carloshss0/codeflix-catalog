import pytest
from uuid import UUID
import uuid
from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match= "missing 1 required positional argument: 'name'"):
            Category()
    def test_empty_name_must_raise_an_exception(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name= "")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match= "name must have less than 256 characters"):
            Category("a"*256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name= "Movie")
        assert isinstance(category.id, UUID)


    def test_create_category_without_optional_fields(self):
        category = Category(name="Serie")
        assert category.name == "Serie"
        assert category.description == ""
        assert category.is_active is True


    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Documentary")
        assert category.is_active is True
    
    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Comedy",
            description="French Comedy",
            is_active=False     
        )
        assert category.id == category_id
        assert category.name == "Comedy"
        assert category.description == "French Comedy"
        assert category.is_active is False

    def test_str_method_for_category(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Comedy",
            description="French Comedy",
            is_active=False     
        )

        string_str = f"{category.id} - {category.name} - {category.description} - {category.is_active}"
        assert str(category) == string_str

    def test_repr_method_for_category(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Comedy",
            description="French Comedy",
            is_active=False     
        )

        string_str = f"<Category {category.id} - {category.name} - {category.description} - {category.is_active}"
        assert repr(category) == string_str


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Film", description="Adventure Film")
        category.update_category(name="Serie", description="Comedy Serie")

        assert category.name == "Serie"
        assert category.description == "Comedy Serie"

    def test_update_category_with_invalid_name_must_raise_exception(self):
        category = Category(name="Film", description="Adventure Film")
        with pytest.raises(ValueError, match= "name must have less than 256 characters"):
            category.update_category(name= "a"*256, description="Adventure Film")

    def test_cannot_update_category_with_empty_name(self):
        category = Category(name="Film", description="Adventure Film")
        with pytest.raises(ValueError, match= "name cannot be empty"):
            category.update_category(name= "", description="Adventure Film")


class TestActivateCategory:
    def test_activate_category(self):
        category = Category(name="Film", description="Adventure Film", is_active=False)
        category.activate()
        assert category.is_active is True

    def test_deactivate_category(self):
        category = Category(name="Film", description="Adventure Film", is_active=True)
        category.deactivate()
        assert category.is_active is False


class TestEqualCategory:
    def test_when_categories_have_same_id_they_are_equal(self):
        category_id = uuid.uuid4()
        category_1 = Category(name= "Movie", id= category_id)
        category_2 = Category(name= "Movie", id= category_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category_1 = Category(name= "Movie", id= common_id)

        dummy = Dummy()
        dummy.id = common_id

        assert category_1 != dummy