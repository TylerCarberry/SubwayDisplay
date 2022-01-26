from dataclasses import dataclass
from datetime import datetime
from typing import List

from utils import get_minutes_until_arrival


@dataclass
class Direction:
    name: str
    arrival_timestamps: List[int]

    def get_header_text(self) -> str:
        if len(self.arrival_timestamps) == 0:
            return self.name

        next_arrival_time: int = get_minutes_until_arrival(self.arrival_timestamps[0])

        return "{} - {} {}".format(
            self.name,
            next_arrival_time,
            "min" if next_arrival_time == 1 else "mins"
        )

    def get_also_text(self) -> str:
        if len(self.arrival_timestamps) == 0:
            return "No upcoming trains"
        if len(self.arrival_timestamps) == 1:
            return ""

        times = []
        for timestamp in self.arrival_timestamps[1:5]:
            time_obj = datetime.fromtimestamp(timestamp)
            times.append(time_obj.strftime("%-I:%M"))
        return "Also " + ", ".join(times)
