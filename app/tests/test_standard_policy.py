import unittest
from datetime import datetime
from app.interfaces import VehicleType
from app.models import ParkingSession
from app.engine import calculate_fee

class TestParkingCalculator(unittest.TestCase):

    def test_standard_1hr_nonpeak_car(self):
        """CAR: 1 hour stay, no peak surcharge."""
        # Monday 12:00 PM - 1:00 PM
        s = ParkingSession(datetime(2026, 2, 9, 12, 0), datetime(2026, 2, 9, 13, 0), VehicleType.CAR)
        # Expected: $5.00 base * 1.0 vehicle multiplier
        self.assertEqual(calculate_fee(s), 5.0)

    def test_standard_3hrs_nonpeak_car(self):
        """CAR: 3 hour stay, no peak surcharge."""
        # Monday 12:00 PM - 3:00 PM
        s = ParkingSession(datetime(2026, 2, 9, 12, 0), datetime(2026, 2, 9, 15, 0), VehicleType.CAR)
        # Expected: ($5 + $3 + $2) = $10.00
        self.assertEqual(calculate_fee(s), 10.0)

    def test_standard_peak_exact_match(self):
        """CAR: 1 hour stay exactly during peak window (7-8 AM)."""
        s = ParkingSession(datetime(2026, 2, 9, 7, 0), datetime(2026, 2, 9, 8, 0), VehicleType.CAR)
        # Expected: $5.00 * 1.5 multiplier = $7.50
        self.assertEqual(calculate_fee(s), 7.50)

    def test_standard_peak_partial_overlap(self):
        """CAR: 1 hr 5 min stay starting before peak (3:30-4:35 PM)."""
        # Rounds to 2 hours.
        # Hour 1 (3:30-4:30) overlaps 4 PM peak start -> $5.0 * 1.5 = $7.5
        # Hour 2 (4:30-5:30) is in peak -> $3.0 * 1.5 = $4.5
        s = ParkingSession(datetime(2026, 2, 9, 15, 30), datetime(2026, 2, 9, 16, 35), VehicleType.CAR)
        self.assertEqual(calculate_fee(s), 12.0)

    def test_standard_1hr_motorcycle(self):
        """MOTORCYCLE: 0.8x multiplier applied to 1hr base ($5)."""
        s = ParkingSession(datetime(2026, 2, 9, 12, 0), datetime(2026, 2, 9, 13, 0), VehicleType.MOTOR_CYCLE)
        # Expected: $5.00 * 0.8 = $4.00
        self.assertEqual(calculate_fee(s), 4.00)

    def test_standard_1hr_bus_peak(self):
        """BUS: 2.0x multiplier applied to 1hr peak stay ($5 * 1.5 surcharge)."""
        s = ParkingSession(datetime(2026, 2, 9, 7, 0), datetime(2026, 2, 9, 8, 0), VehicleType.BUS)
        # Expected: ($5.00 * 1.5) * 2.0 = $15.00
        self.assertEqual(calculate_fee(s), 15.00)

    def test_standard_rounding_61_minutes(self):
        """Verify 61 minutes rounds to 2 full hours."""
        # 12:00 PM to 1:01 PM
        s = ParkingSession(datetime(2026, 2, 9, 12, 0), datetime(2026, 2, 9, 13, 1), VehicleType.CAR)
        # Expected: $5 (Hr 1) + $3 (Hr 2) = $8.00
        self.assertEqual(calculate_fee(s), 8.00)

    def test_standard_loyalty_no_impact(self):
        """Verify Loyalty does NOT apply to Standard rates (as per requirements)."""
        s = ParkingSession(datetime(2026, 2, 9, 12, 0), datetime(2026, 2, 9, 13, 0), VehicleType.CAR,
                           loyalty="PLATINUM")
        # Expected: Still $5.00 (Standard policy does not list loyalty discounts)
        self.assertEqual(calculate_fee(s), 5.0)

if __name__ == '__main__':
    unittest.main()