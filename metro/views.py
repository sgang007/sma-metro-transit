from django.http import JsonResponse
from django.views.generic import TemplateView
import pandas as pd
import io
from .models import Journey
from django.shortcuts import render
from .fare_calculator import FareCalculator
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def calculate_fare(request):
    try:
        # Query the DB for available route information
        source = request.GET.get("from")
        destination = request.GET.get("to")
        date = request.GET.get("date")
        if not source or not destination or not date:
            return JsonResponse({"error": "Invalid Parameters"}, status=400)

        # Atomic Transaction reverts in case of errors
        with transaction.atomic():
            calculator = FareCalculator(source, destination, date)
            fare = calculator.calculate_fare()
            # Save the journey information for calculating weekly discounts in future
            Journey.objects.create(source=calculator.source,
                                   destination=calculator.destination,
                                   date=calculator.date,
                                   fare=fare)
            return JsonResponse({"fare": fare})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


class CsvUploader(TemplateView):
    template_name = 'csv_uploader.html'

    @method_decorator(csrf_exempt)
    def post(self, request):
        context = {
            'messages': [],
            'data': []
        }

        csv = request.FILES['csv']
        csv_data = pd.read_csv(
            io.StringIO(
                csv.read().decode("utf-8")
            )
        )

        for record in csv_data.to_dict(orient="records"):
            try:
                with transaction.atomic():
                    calculator = FareCalculator(record['from'], record['to'], record['date'])
                    fare = calculator.calculate_fare()
                    trip = Journey.objects.create(source=calculator.source,
                                           destination=calculator.destination,
                                           date=calculator.date,
                                           fare=fare)
                    context['messages'].append(
                        f"Journey from {record['from']} to {record['to']} on {record['date']} costs ${fare}"
                    )
                    context['data'].append(trip)

            except Exception as e:
                context['exceptions_raised'] = e

        return render(request, self.template_name, context)

