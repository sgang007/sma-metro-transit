from metro.models import *
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Clear all existing data
        Journey.objects.all().delete()
        Traffic.objects.all().delete()
        Route.objects.all().delete()
        Line.objects.all().delete()

        # Setup Lines
        l1 = Line.objects.create(name="Red")
        l2 = Line.objects.create(name="Green")
        l3 = Line.objects.create(name="Grey")
        l4 = Line.objects.create(name="Yellow")

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

        self.stdout.write(self.style.SUCCESS('Successfully loaded fare rules'))
