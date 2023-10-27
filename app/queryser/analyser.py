from dataclasses import dataclass
import math

@dataclass
class Cost:
    equation: str
    value: float
    
def primary_key_cost(size: int) -> Cost:
    """
    Cost of querying a primary key column
    Table would be sorted by the primary key column
    An index would be used to find the row
    We should be to search the index in O(log(n)) time
    Then read the row in O(1) time
    """
    return Cost(
        equation="log(n) + 1",
        value=math.log(size, 2) + 1,
    )

def secondary_key_cost(size: int) -> Cost:
    """
    Cost of querying a secondary key column
    An B+ index would be used to find the row
    We should be to search the index in height of the tree
    Then read the row in O(1) time
    """
    return Cost(
        equation="h + 1",
        value=math.log(size, 2) + 1,
    )