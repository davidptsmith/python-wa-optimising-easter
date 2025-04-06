from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Child:
    name: str
    age: int
    basket_capacity: int
    preference: Dict[str, bool]
    house_id: int

    def effective_time(self, base_time=15, age_handicap_per_year=0.5, age_threshold=10) -> float:
        extra_time = max(0, self.age - age_threshold) * age_handicap_per_year
        return max(0, base_time - extra_time)