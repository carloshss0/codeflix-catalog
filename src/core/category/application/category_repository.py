from abc import ABC, abstractmethod

class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError