from dataclasses import dataclass, field
from typing import Dict, List
from Optimiser.Child import Child

@dataclass
class House:
    id: int
    children: List[Child]