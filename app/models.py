# app/models.py
from dataclasses import dataclass
from datetime import datetime
from app.interfaces import VehicleType, LoyaltyTier

@dataclass
class ParkingSession:
    entry: datetime
    exit: datetime
    vehicle: VehicleType
    loyalty: LoyaltyTier = LoyaltyTier.NONE

    @property
    def duration_hours(self) -> float:
        delta = self.exit - self.entry
        return delta.total_seconds() / 3600