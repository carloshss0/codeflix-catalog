from dataclasses import dataclass, field
import uuid
from uuid import UUID

@dataclass
class Category:
    name: str
    description: str = ""
    is_activate: bool = True
    id: UUID = field(default_factory= uuid.uuid4)

    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characters")
        
        if not self.name:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.description} - {self.is_activate}"
    
    def __repr__(self):
        return f"<Category {self.id} - {self.name} - {self.description} - {self.is_activate}"
    
    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        
        return self.id == other.id
    
    def update_category(self, name, description):        
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_activate = True

        self.validate()
    
    def deactivate(self):
        self.is_activate = False
        
        self.validate()