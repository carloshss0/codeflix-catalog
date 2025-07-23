from uuid import UUID
from core.category.application.category_repository import CategoryRepository
from core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel):
        self.category_model = category_model

    def save(self, category: Category) -> None:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_activate=category.is_activate
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.category_model.objects.get(id=id)
            return Category(
                id=category_model.id,
                name=category_model.name,
                description=category_model.description,
                is_activate=category_model.is_activate
            )
        except self.category_model.DoesNotExist:
            return None
    
    def delete(self, id: UUID) -> None:
        try:
            category_model = self.category_model.objects.get(id=id)
            category_model.delete()
        except self.category_model.DoesNotExist:
            pass
    
    def list(self) -> list[Category]:
        categories = self.category_model.objects.all()
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_activate=category.is_activate
            ) for category in categories
        ]
    
    def update(self, category: Category) -> Category:
        category_id = category.id
        try:
            category_model = self.category_model.objects.get(id=category_id)
            category_model.name = category.name
            category_model.description = category.description
            category_model.is_activate = category.is_activate
            category_model.save()
            return Category(
                id=category_model.id,
                name=category_model.name,
                description=category_model.description,
                is_activate=category_model.is_activate
            )
        except self.category_model.DoesNotExist:
            return None