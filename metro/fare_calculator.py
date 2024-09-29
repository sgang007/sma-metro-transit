from .models import *
from django.utils import dateparse
from datetime import timedelta
from django.utils.timezone import is_aware, make_aware


class FareCalculator:
    def __init__(self, source, destination, date):
        self.source = Line.objects.get(name=source.title())
        self.destination = Line.objects.get(name=destination.title())
        self.date = dateparse.parse_datetime(date)
        if not is_aware(self.date):
            self.date = make_aware(self.date)

    def apply_daily_cap(self, fare, route):
        history = Journey.objects.filter(source=self.source,
                                         destination=self.destination,
                                         date__year=self.date.year,
                                         date__month=self.date.month,
                                         date__day=self.date.day)
        old_fares = sum([journey.fare for journey in history])
        if old_fares + fare >= route.daily_cap:
            discount = old_fares + fare - route.daily_cap
            fare -= discount
            fare = max(fare, 0)
        return fare

    def apply_weekly_cap(self, fare, route):
        history = Journey.objects.filter(source=self.source,
                                         destination=self.destination,
                                         date__year=self.date.year,
                                         date__gte=self.date - timedelta(days=7))
        old_fares = sum([journey.fare for journey in history])
        if old_fares + fare >= route.weekly_cap:
            discount = old_fares + fare - route.weekly_cap
            fare -= discount
            fare = max(fare, 0)
        return fare

    def calculate_fare(self):
        # Logic to calculate fare
        # If conflicting route information is available, use the latest one
        route = Route.objects.filter(source=self.source, destination=self.destination).last()
        if not route:
            raise Exception("No Route Found")

        # Check for peak hours and calculate fare
        time = self.date.time()
        weekday = Traffic.Day(str(self.date.weekday() + 1))
        peak_traffic = Traffic.objects.filter(day=weekday,
                                              from_time__lte=time,
                                              to_time__gte=time,
                                              peak_hours=True)
        fare = route.peak_hours_price if peak_traffic.exists() else route.off_peak_hours_price

        # Apply daily cap
        fare = self.apply_daily_cap(fare, route)

        # Apply weekly cap
        fare = self.apply_weekly_cap(fare, route)

        return fare


