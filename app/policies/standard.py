import math
from datetime import datetime, timedelta, time
from app.interfaces import IParkingPolicy


class StandardPolicy(IParkingPolicy):
    def __init__(self):
        self.base_rates = {1: 5.0, 2: 3.0, 3: 2.0}
        self.peak_multiplier = 1.5

    def is_applicable(self, session) -> bool:

        return True

    def _is_peak_hour(self, segment_start: datetime) -> bool:
        if segment_start.weekday() > 4:  # Weekdays only
            return False

        segment_end = segment_start + timedelta(hours=1)

        peak_windows = [
            (time(7, 0), time(10, 0)),
            (time(16, 0), time(19, 0))
        ]

        for p_start, p_end in peak_windows:
            p_start_dt = datetime.combine(segment_start.date(), p_start)
            p_end_dt = datetime.combine(segment_start.date(), p_end)

            if segment_start < p_end_dt and segment_end > p_start_dt:
                return True

        return False

    def calculate_fee(self, session) -> float:
        total_hours = math.ceil(session.duration_hours)
        total_fee = 0.0

        for i in range(1, total_hours + 1):

            hourly_base = self.base_rates.get(i, self.base_rates[3])
            segment_start = session.entry + timedelta(hours=i - 1)

            multiplier = self.peak_multiplier if self._is_peak_hour(segment_start) else 1.0
            total_fee += (hourly_base * multiplier)

        return total_fee * session.vehicle.value