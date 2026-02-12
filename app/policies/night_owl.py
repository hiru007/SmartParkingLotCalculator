from datetime import time, timedelta
from app.interfaces import IParkingPolicy


class NightOwlPolicy(IParkingPolicy):
    def __init__(self):
        self.flat_rate = 8.0
        # Entry: 6:00 PM – 11:59 PM
        self.entry_start = time(18, 0)
        self.entry_end = time(23, 59)
        # Exit: 5:00 AM – 10:00 AM (Next Day)
        self.exit_start = time(5, 0)
        self.exit_end = time(10, 0)

    def is_applicable(self, session) -> bool:
        if session.duration_hours > 18 or session.duration_hours > 24:
            return False

        if session.exit.date() != session.entry.date() + timedelta(days=1):
            return False

        entry_time = session.entry.time()
        valid_entry = self.entry_start <= entry_time <= self.entry_end

        exit_time = session.exit.time()
        valid_exit = self.exit_start <= exit_time <= self.exit_end

        return valid_entry and valid_exit

    def calculate_fee(self, session) -> float:
        discounted_flat_rate = self.flat_rate * (1 - session.loyalty.value)
        return discounted_flat_rate * session.vehicle.value