import unittest
from datetime import datetime
from app.interfaces import VehicleType, LoyaltyTier
from app.models import ParkingSession
from app.engine import calculate_fee


class TestParkingCalculator(unittest.TestCase):

    def test_night_owl_valid_consecutive_day_car(self):
        """CAR: Valid window (Entry Mon 8 PM, Exit Tue 6 AM) next day"""
        # Monday to Tuesday
        entry = datetime(2026, 2, 9, 20, 0)
        exit = datetime(2026, 2, 10, 6, 0)  # 10 hours total
        s = ParkingSession(entry, exit, VehicleType.CAR)
        self.assertEqual(calculate_fee(s), 8.0)

    def test_night_owl_invalid_exit_time(self):
        """CAR: Exit at 4:59 AM (too early) should fall back to Standard."""
        entry = datetime(2026, 2, 9, 20, 0)
        exit = datetime(2026, 2, 10, 4, 59)  # Before 5 AM window
        s = ParkingSession(entry, exit, VehicleType.CAR)

        self.assertNotEqual(calculate_fee(s), 8.0)
        self.assertEqual(calculate_fee(s), 22)

    def test_night_owl_exceeds_18_hours(self):
        """CAR: Valid windows but duration is 18.5 hours (Invalid)."""
        # Entry 6:00 PM, Exit 12:30 PM next day (Exit window is 5-10 AM)
        entry = datetime(2026, 2, 9, 18, 0)
        exit = datetime(2026, 2, 10, 12, 30)
        s = ParkingSession(entry, exit, VehicleType.CAR)
        self.assertNotEqual(calculate_fee(s), 8.0)
        self.assertEqual(calculate_fee(s), 47.5)

    def test_night_owl_motorcycle(self):
        """MOTORCYCLE: 0.8x multiplier applied to $8 flat rate[."""
        entry = datetime(2026, 2, 9, 20, 0)
        exit = datetime(2026, 2, 10, 6, 0)
        s = ParkingSession(entry, exit, VehicleType.MOTOR_CYCLE)
        # Expected: $8.00 * 0.8 = $6.40
        self.assertEqual(calculate_fee(s), 6.40)

    def test_night_owl_bus(self):
        """BUS: 2.0x multiplier applied to $8 flat rate."""
        entry = datetime(2026, 2, 9, 20, 0)
        exit = datetime(2026, 2, 10, 6, 0)
        s = ParkingSession(entry, exit, VehicleType.BUS)
        # Expected: $8.00 * 2.0 = $16.00
        self.assertEqual(calculate_fee(s), 16.00)

    def test_night_owl_silver_car(self):
        """CAR: Silver (10% discount) on $8 flat rate."""
        s = ParkingSession(datetime(2026, 2, 9, 20, 0), datetime(2026, 2, 10, 6, 0),
                           VehicleType.CAR, loyalty=LoyaltyTier.SILVER)
        # Expected: $8.00 - 10% = $7.20
        self.assertEqual(calculate_fee(s), 7.20)

    def test_night_owl_platinum_car(self):
        """CAR: Platinum (30% discount) on $8 flat rate."""
        s = ParkingSession(datetime(2026, 2, 9, 20, 0), datetime(2026, 2, 10, 6, 0),
                           VehicleType.CAR, loyalty=LoyaltyTier.PLATINUM)
        # Expected: $8.00 - 30% = $5.60
        self.assertEqual(calculate_fee(s), 5.60)

    def test_night_owl_gold_motorcycle(self):
        """MOTORCYCLE: Gold (20% discount) on $8 base, then 0.8x multiplier."""
        entry = datetime(2026, 2, 9, 20, 0)
        exit = datetime(2026, 2, 10, 6, 0)
        s = ParkingSession(entry, exit, VehicleType.MOTOR_CYCLE, loyalty=LoyaltyTier.GOLD)

        # Calculation: ($8.00 * 0.8 loyalty) * 0.8 vehicle multiplier = $5.12
        expected_fee = 5.12
        self.assertAlmostEqual(calculate_fee(s), expected_fee, places=2)


if __name__ == '__main__':
    unittest.main()