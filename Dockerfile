FROM python:3.10.5
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py test
RUN python manage.py  load_fare_rules
CMD [ "sh","-c", " python manage.py createsuperuser --noinput && gunicorn --bind 0.0.0.0:8000 --workers 2 sma_metro_transit.wsgi"]