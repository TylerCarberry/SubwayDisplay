from dataclasses import dataclass
from typing import List
from server.model.direction import Direction


@dataclass
class Line:
    letter: str  # Ex. (A,C,E,1,2,3)
    uptown: Direction
    downtown: Direction
    alerts: List[str]
