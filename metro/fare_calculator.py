from .models import *
from django.utils import dateparse


class FareCalculator:
    def __init__(self, source, destination, date):
        self.source = Line.objects.get(name=source.title())
        self.destination = Line.objects.get(name=destination.title())
        self.date = dateparse.parse_datetime(date)

    def calculate_fare(self):
        # Logic to calculate fare
        # If conflicting route information is available, use the latest one
        route = Route.objects.filter(source=self.source, destination=self.destination).last()
        if not route:
            raise Exception("No Route Found")

        # Check for peak hours and calculate fare
        time = self.date.time()
        peak_traffic = Traffic.objects.filter(from_time__lte=time, to_time__gte=time, peak_hours=True)
        fare = route.peak_hours_price if peak_traffic.exists() else route.off_peak_hours_price

        # Apply daily cap
        fare = min(route.daily_cap, fare)

        # Apply weekly cap
        history = Journey.objects.filter(source=self.source,
                                         destination=self.destination,
                                         date__week=self.date.isocalendar()[1])
        if history.exists():
            total_fares = fare + sum([journey.fare for journey in history])
        else:
            total_fares = fare

        if total_fares >= route.weekly_cap:
            discount = total_fares - route.weekly_cap
            fare -= discount
            fare = max(fare, 0)

        return fare

