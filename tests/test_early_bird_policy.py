import unittest
from datetime import datetime
from app.interfaces import VehicleType, LoyaltyTier
from app.models import ParkingSession
from app.engine import calculate_fee


class TestParkingCalculator(unittest.TestCase):

    def test_early_bird_exact_window_car(self):
        """CAR: Valid window (Entry 7 AM, Exit 4 PM) same day."""
        # Monday, Feb 9, 2026
        entry = datetime(2026, 2, 9, 7, 0)
        exit = datetime(2026, 2, 9, 16, 0)
        s = ParkingSession(entry, exit, VehicleType.CAR)

        self.assertEqual(calculate_fee(s), 15.0)

    def test_early_bird_invalid_entry_time(self):
        """CAR: Entry at 5:59 AM (too early) should fall back to Standard."""
        entry = datetime(2026, 2, 9, 5, 59)
        exit = datetime(2026, 2, 9, 16, 0)
        s = ParkingSession(entry, exit, VehicleType.CAR)
        self.assertEqual(calculate_fee(s), 31.5)

    def test_early_bird_exceeds_15_hours(self):
        """CAR: Valid windows but duration is 15.5 hours (Invalid)."""

        # Entry 6:00 AM, Exit 9:30 PM (Next window technically, but > 15 hrs)
        entry = datetime(2026, 2, 9, 6, 0)
        exit = datetime(2026, 2, 9, 21, 30)
        s = ParkingSession(entry, exit, VehicleType.CAR)
        self.assertNotEqual(calculate_fee(s), 15.0)
        self.assertEqual(calculate_fee(s), 42.5)

    def test_early_bird_motorcycle(self):
        """MOTORCYCLE: 0.8x multiplier applied to $15 flat rate."""
        entry = datetime(2026, 2, 9, 7, 0)
        exit = datetime(2026, 2, 9, 16, 0)
        s = ParkingSession(entry, exit, VehicleType.MOTOR_CYCLE)
        self.assertEqual(calculate_fee(s), 12.0)

    def test_early_bird_bus(self):
        """BUS: 2.0x multiplier applied to $15 flat rate."""
        entry = datetime(2026, 2, 9, 7, 0)
        exit = datetime(2026, 2, 9, 16, 0)
        s = ParkingSession(entry, exit, VehicleType.BUS)
        self.assertEqual(calculate_fee(s), 30.0)

    def test_early_bird_silver_car(self):
        """CAR: Silver (10% discount) on $15 flat rate."""
        s = ParkingSession(datetime(2026, 2, 9, 7, 0), datetime(2026, 2, 9, 16, 0),
                           VehicleType.CAR, loyalty=LoyaltyTier.SILVER)
        # Expected: $15.00 - 10% = $13.50
        self.assertEqual(calculate_fee(s), 13.5)

    def test_early_bird_gold_car(self):
        """CAR: Gold (20% discount) on $15 flat rate."""
        s = ParkingSession(datetime(2026, 2, 9, 7, 0), datetime(2026, 2, 9, 16, 0),
                           VehicleType.CAR, loyalty=LoyaltyTier.GOLD)
        # Expected: $15.00 - 20% = $12.00
        self.assertEqual(calculate_fee(s), 12.0)

    def test_early_bird_platinum_car(self):
        """CAR: Platinum (30% discount) on $15 flat rate."""
        s = ParkingSession(datetime(2026, 2, 9, 7, 0), datetime(2026, 2, 9, 16, 0),
                           VehicleType.CAR, loyalty=LoyaltyTier.PLATINUM)
        # Expected: $15.00 - 30% = $10.50
        self.assertEqual(calculate_fee(s), 10.5)

    def test_early_bird_platinum_bus(self):
        """BUS: Platinum (30% discount) on $15 flat rate, then 2.0x multiplier."""
        entry = datetime(2026, 2, 9, 7, 0)
        exit = datetime(2026, 2, 9, 16, 0)
        s = ParkingSession(entry, exit, VehicleType.BUS, loyalty=LoyaltyTier.PLATINUM)
        # Calculation: ($15.00 * 0.7 discount) * 2.0 multiplier = $10.50 * 2 = $21.00
        self.assertEqual(calculate_fee(s), 21.0)


if __name__ == '__main__':
    unittest.main()