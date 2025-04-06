from dataclasses import dataclass

@dataclass
class EggType:
    name: str
    value: int
    enjoyment: int
    health: int
    size: int
    cost: int