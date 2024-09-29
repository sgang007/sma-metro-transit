from django.test import TestCase
from .models import *
from .fare_calculator import FareCalculator
from datetime import timedelta

# Create your tests here.


class FareCalculatorTest(TestCase):
    def setUp(self):
        l1 = Line.objects.create(name="Red")
        l2 = Line.objects.create(name="Green")
        # Setup Fare Rules
        Route.objects.create(source=l1,
                             destination=l2,
                             peak_hours_price=3,
                             off_peak_hours_price=2,
                             daily_cap=15,
                             weekly_cap=90)
        Route.objects.create(source=l2,
                             destination=l1,
                             peak_hours_price=4,
                             off_peak_hours_price=3,
                             daily_cap=15,
                             weekly_cap=90)
        Route.objects.create(source=l1,
                             destination=l1,
                             peak_hours_price=3,
                             off_peak_hours_price=2,
                             daily_cap=12,
                             weekly_cap=70)
        Route.objects.create(source=l2,
                             destination=l2,
                             peak_hours_price=2,
                             off_peak_hours_price=1,
                             daily_cap=8,
                             weekly_cap=55)
        # Setup Peak Hours
        weekdays = [Traffic.Day.MON, Traffic.Day.TUE, Traffic.Day.WED, Traffic.Day.THU, Traffic.Day.FRI]
        for day in weekdays:
            Traffic.objects.create(day=day,
                                   from_time='08:00:00',
                                   to_time='10:00:00',
                                   peak_hours=True)
            Traffic.objects.create(day=day,
                                   from_time='16:30:00',
                                   to_time='19:00:00',
                                   peak_hours=True)
        Traffic.objects.create(day=Traffic.Day.SAT,
                               from_time='10:00:00',
                               to_time='14:00:00',
                               peak_hours=True)
        Traffic.objects.create(day=Traffic.Day.SAT,
                               from_time='18:00:00',
                               to_time='23:00:00',
                               peak_hours=True)
        Traffic.objects.create(day=Traffic.Day.SUN,
                               from_time='18:00:00',
                               to_time='23:00:00',
                               peak_hours=True)
        Journey.objects.all().delete()

    def test_peak_hours(self):
        print("Testing peak hours")
        # Sunday
        assert FareCalculator("Red", "Green", "2024-09-01T19:30:00").calculate_fare() == 3
        # Saturday
        assert FareCalculator("Red", "Green", "2024-09-07T12:30:00").calculate_fare() == 3
        # Weekdays
        assert FareCalculator("Red", "Green", "2024-09-03T09:30:00").calculate_fare() == 3
        pass

    def test_off_peak_hours(self):
        print("Testing off peak hours")
        # Sunday
        assert FareCalculator("Red", "Green", "2024-09-01T10:30:00").calculate_fare() == 2
        # Saturday
        assert FareCalculator("Red", "Green", "2024-09-07T15:30:00").calculate_fare() == 2
        # Weekdays
        assert FareCalculator("Red", "Green", "2024-09-03T12:30:00").calculate_fare() == 2
        pass

    def test_daily_cap(self):
        print("Testing daily cap")
        date = "2024-09-03T01:00:00"
        # Run fare every 30 minutes for 23 hours
        for i in range(45):
            calculator = FareCalculator("Red", "Green", date)
            fare = calculator.calculate_fare()
            Journey.objects.create(source=calculator.source,
                                   destination=calculator.destination,
                                   date=calculator.date,
                                   fare=fare)
            date = (calculator.date + timedelta(minutes=30)).isoformat()
        assert sum(Journey.objects.all().values_list('fare', flat=True)) == 15
        pass

    def test_weekly_cap(self):
        print("Testing weekly cap")
        date = "2024-09-01T01:00:00"
        # Run fare every 30 minutes for 7 days
        for i in range(7 * 48):
            calculator = FareCalculator("Red", "Green", date)
            fare = calculator.calculate_fare()
            Journey.objects.create(source=calculator.source,
                                   destination=calculator.destination,
                                   date=calculator.date,
                                   fare=fare)
            date = (calculator.date + timedelta(minutes=30)).isoformat()
        assert sum(Journey.objects.all().values_list('fare', flat=True)) == 90
        pass
