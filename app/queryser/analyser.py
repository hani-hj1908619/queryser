from dataclasses import dataclass
import math

@dataclass
class Cost:
    equation: str
    value: float
    
def primary_key_cost(size: int) -> Cost:
    return Cost(
        equation="log(n)",
        value=math.log(size, 2),
    )

def secondary_key_cost(size: int) -> Cost:
    return Cost(
        equation="h + 1",
        value=math.log(size, 2) + 1,
    )

def primary_key_range_cost(size: int, range_size: int) -> Cost:
    return Cost(
        equation="log(n) + r",
        value=math.log(size, 2) + range_size,
    )

def secondary_key_range_cost(size: int, range_size: int) -> Cost:
    return Cost(
        equation="h + r + 1",
        value=math.log(size, 2) + range_size + 1,
    )