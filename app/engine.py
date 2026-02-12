from app.models import ParkingSession
from app.policies.standard import StandardPolicy
from app.policies.early_bird import EarlyBirdPolicy
from app.policies.night_owl import NightOwlPolicy


def calculate_fee(session: ParkingSession) -> float:
    policies = [
        StandardPolicy(),
        EarlyBirdPolicy(),
        NightOwlPolicy()
    ]


    fees = [
        p.calculate_fee(session)
        for p in policies if p.is_applicable(session)
    ]

    return min(fees) if fees else 0.0