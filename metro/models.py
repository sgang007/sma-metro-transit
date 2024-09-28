from django.db import models


class Line(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField(default=0.0)
    opening_hours = models.TimeField(default='00:00:00')
    closing_hours = models.TimeField(default='23:00:00')

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100)
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='stations')
    locality = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    is_junction = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='destination')
    peak_hours_price = models.FloatField(default=0.0)
    off_peak_hours_price = models.FloatField(default=0.0)
    daily_cap = models.FloatField(default=0.0)
    weekly_cap = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.source} to {self.destination}'


class Traffic(models.Model):
    class Day(models.TextChoices):
        MON = "1", "MONDAY"
        TUE = "2", "TUESDAY"
        WED = "3", "WEDNESDAY"
        THU = "4", "THURSDAY"
        FRI = "5", "FRIDAY"
        SAT = "6", "SATURDAY"
        SUN = "7", "SUNDAY"
    day = models.CharField(max_length=1, choices=Day.choices)
    from_time = models.TimeField(default='00:00:00')
    to_time = models.TimeField(default='23:00:00')
    peak_hours = models.BooleanField(default=True)

    def __str__(self):
        return f'{Traffic.Day(self.day).label} from {self.from_time} to {self.to_time}'


class Journey(models.Model):
    card_id = models.CharField(max_length=100, blank=True, null=True)
    source = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='journey_source')
    destination = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='journey_destination')
    date = models.DateTimeField()
    fare = models.FloatField()

    def __str__(self):
        return f'${self.fare} : {self.source} to {self.destination}  |  {self.date.strftime("%d/%m/%Y, %H:%M")}'

