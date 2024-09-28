from django.http import JsonResponse
from django.utils import dateparse
from .models import *


# Create your views here.
def calculate_fare(request):
    try:
        # Query the DB for available route information
        source = request.GET.get("from")
        destination = request.GET.get("to")
        time = request.GET.get("time")
        if not source or not destination or not time:
            return JsonResponse({"error": "Invalid Parameters"}, status=400)
        source = Line.objects.get(name=source)
        destination = Line.objects.get(name=destination)
        time = dateparse.parse_datetime(time).time()

        # If conflicting route information is available, use the latest one
        route = Route.objects.filter(source=source, destination=destination).last()
        if not route:
            return JsonResponse({"error": "No Route Found"}, status=404)

        # Check for peak hours and calculate fare
        traffic = Traffic.objects.filter(from_time__lte=time, to_time__gte=time)
        if traffic.exists():
            fare = route.peak_hours_price if traffic.last().peak_hours else route.off_peak_hours_price
        else:
            fare = route.off_peak_hours_price

        # Apply daily cap
        fare = min(route.daily_cap, fare)

        # Apply weekly cap
        history = Journey.objects.filter(source=source, destination=destination)
        if history.exists():
            total_fares = fare + sum([journey.fare for journey in history])
        else:
            total_fares = fare

        if total_fares >= route.weekly_cap:
            discount = total_fares - route.weekly_cap
            fare -= discount
            fare = max(fare, 0)

        # Save the journey information for calculating weekly discounts in future
        Journey.objects.create(source=source, destination=destination, time=time, fare=fare)

        return JsonResponse({"fare": fare})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


