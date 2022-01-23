from dataclasses import dataclass
from typing import List


@dataclass()
class ArrivalTimes:
    line_letter: str
    stop_number: int
    direction: str
    arrival_times: List[int]

    def __init__(self, line_letter, stop_number, direction, arrival_times=None):
        self.line_letter = line_letter
        self.stop_number = stop_number
        self.direction = direction
        if arrival_times is None:
            self.arrival_times = []
        else:
            self.arrival_times = arrival_times

    def get_stop_id(self):
        return f"{self.line_letter}{self.stop_number}{self.direction}"
