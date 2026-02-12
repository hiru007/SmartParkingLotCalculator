
from abc import ABC, abstractmethod
from enum import Enum

class VehicleType(Enum):
    CAR = 1.0
    BUS = 2.0
    MOTOR_CYCLE = 0.8

class LoyaltyTier(Enum):
    NONE = 0.0
    SILVER = 0.10
    GOLD = 0.20
    PLATINUM = 0.30

class IParkingPolicy(ABC):
    @abstractmethod
    def is_applicable(self, session) -> bool:
        pass

    @abstractmethod
    def calculate_fee(self, session) -> float:
        pass