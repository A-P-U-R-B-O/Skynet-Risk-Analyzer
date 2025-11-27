"""AI System model definition."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class AISystem:
    """Represents an AI system to be analyzed for Skynet risk. 
    
    Attributes:
        name: Name of the AI system
        capabilities: Overall capability level (0-100)
        autonomy_level: Level of autonomous operation (0-100)
        ethical_alignment: Alignment with human values (0-100)
        learning_rate: Speed of learning/adaptation (0-100)
        resource_access: Access to computational/physical resources (0-100)
        self_modification: Ability to modify its own code (0-100)
        transparency: How interpretable the system is (0-100)
        human_oversight: Level of human control/monitoring (0-100)
        value_alignment: Alignment with human values (0-100)
        metadata: Additional custom attributes
    """
    
    name: str
    capabilities: float
    autonomy_level: float
    ethical_alignment: float
    learning_rate: float = 50. 0
    resource_access: float = 50.0
    self_modification: float = 0.0
    transparency: float = 50.0
    human_oversight: float = 50.0
    value_alignment: float = 50.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate attribute ranges."""
        attributes = [
            'capabilities', 'autonomy_level', 'ethical_alignment',
            'learning_rate', 'resource_access', 'self_modification',
            'transparency', 'human_oversight', 'value_alignment'
        ]
        
        for attr in attributes:
            value = getattr(self, attr)
            if not 0 <= value <= 100:
                raise ValueError(f"{attr} must be between 0 and 100, got {value}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'capabilities': self.capabilities,
            'autonomy_level': self.autonomy_level,
            'ethical_alignment': self.ethical_alignment,
            'learning_rate': self.learning_rate,
            'resource_access': self.resource_access,
            'self_modification': self.self_modification,
            'transparency': self.transparency,
            'human_oversight': self.human_oversight,
            'value_alignment': self.value_alignment,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AISystem':
        """Create AISystem from dictionary."""
        return cls(**data)
