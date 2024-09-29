# Singa Metro Transit System
## Introduction
The public transport system for city of Singa - Singa metro authority (SMA) wants to design a
payment system for its service. They allow all banks credit and debit NFC enabled cards to tap at
entry and exit. They also sell NFC enabled rechargeable SmartTap cards.
The metro system is divided into Lines named with different colours. There will be multiple stations
on each line. The fare is calculated based on the Lines you are travelling. There can be more Lines
and more stations coming in the future.

*Note: This code covers how to apply fare rules and calculate prices.
User Management, card management, and other features are not covered in this code.*

![screenhost](https://raw.githubusercontent.com/sgang007/sma-metro-transit/refs/heads/main/Screenshot.png?raw=true)

## Assumptions
1. Only Line to Line travel is allowed. Stations are not used.
2. All trips belong to the same NFC Card.

## Pre-requisites
Install Docker daemon: [Docker Installation](https://docs.docker.com/get-docker/)

## Starting the Application
1. Clone the repository
2. Build the docker image: `docker build -t singa-metro .`
3. Run the application: `docker run -it -p 8000:8000 -e DJANGO_SUPERUSER_USERNAME=admin -e DJANGO_SUPERUSER_PASSWORD=123 -e DJANGO_SUPERUSER_EMAIL=admin@example.com singa-metro `

## Configuration
1. Login to Admin Panel with user `admin` and  password `123`: [Admin Panel](http://localhost:8000/admin/metro/)
2. Configure Lines: [Add / Remove New Lines](http://localhost:8000/admin/metro/line/)
3. Configure peak hours: [Change Traffic Hours](http://localhost:8000/admin/metro/line/)
4. Configure fare rules: [Change fare rules](http://localhost:8000/admin/metro/fare/)

## API Endpoints
1. `/metro/calculate-fare/` - GET - Calculate Fare
    - URL Query Params:
        - `from`: Line where the user enters the metro
        - `to`: Line where the user exits the metro
        - `date`: Date and Time of the journey in ISO format
    - Example: [http://localhost:8000/metro/calculate-fare/?from=red&to=green&date=2021-03-24T09:58:30](http://localhost:8000/metro/calculate-fare/?from=red&to=green&date=2021-03-24T09:58:30)
    - Response:
    ```json
    {
        "fare": 5.0
    }
    ```
   
## CSV Bulk Upload Application
1. Open the browser and navigate to [http://localhost:8000/metro](http://localhost:8000/metro/)
2. Upload the CSV file with the following format. See `test.csv` for example:
    - `from, to, date`
    - Example:
    ```
    red,green,2021-03-24T09:58:30
    green,blue,2021-05-2T19:58:30
    ```
3. Click on the `Upload` button to calculate the fare for each journey.
