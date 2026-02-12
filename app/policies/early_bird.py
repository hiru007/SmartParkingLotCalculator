from datetime import time
from app.interfaces import IParkingPolicy


class EarlyBirdPolicy(IParkingPolicy):
    def __init__(self):
        self.flat_rate = 15.0
        self.entry_start = time(6, 0)
        self.entry_end = time(9, 0)
        self.exit_start = time(15, 30)
        self.exit_end = time(19, 0)

    def is_applicable(self, session) -> bool:

        if session.duration_hours > 15 or session.duration_hours > 24:
            return False

        if session.entry.date() != session.exit.date():
            return False

        entry_time = session.entry.time()
        valid_entry = self.entry_start <= entry_time <= self.entry_end

        exit_time = session.exit.time()
        valid_exit = self.exit_start <= exit_time <= self.exit_end

        return valid_entry and valid_exit

    def calculate_fee(self, session) -> float:
        discounted_flat_rate = self.flat_rate * (1 - session.loyalty.value)

        return discounted_flat_rate * session.vehicle.value