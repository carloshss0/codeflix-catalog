from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID
import uuid

class CastMemberType(StrEnum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"

@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory= uuid.uuid4)

    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characters")
        
        if not self.name:
            raise ValueError("name cannot be empty")
        
        if not isinstance(self.type, CastMemberType):
            raise ValueError("type must be either 'DIRECTOR' or 'ACTOR'")
        

    def __str__(self):
        return f"{self.id} - {self.name} - {self.type}"
    
    def __repr__(self):
        return f"<Cast Member {self.id} - {self.name} - {self.type}"
    
    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        
        return self.id == other.id
    
    def update_cast_member(self, name: str, type: CastMemberType) -> None:
        self.name = name
        self.type = type
        self.validate()