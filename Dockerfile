FROM python:3.10.5
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
RUN python manage.py makemigrations && python manage.py migrate
CMD [ "sh","-c", "python3 manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 sma_metro_transit.wsgi"]