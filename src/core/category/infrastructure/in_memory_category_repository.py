from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.application.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []

    def save(self, category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category:
        for category in self.categories:
            if category.id == id:
                return category
        return None

    def delete(self, id: UUID) -> None:
        for category in self.categories:
            if category.id == id:
                self.categories.remove(category)
                return
        return None
    
    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)    
        
    
