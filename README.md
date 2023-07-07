# Fly-High - a flight booking System

Flight booking web application for booking Flights for user and adding flights by admin.

## User
* User sign in/login
* Book Flights
* See all bookings
* Search flights based on destination, date, time, origin

## Admin
* Login
* Add/delete Flights
* Check all the flights and corresponding bookings.

## Tech Stack 

### Frontend
* Reactjs (for data rendering and state management)
* TailwindCSS (for design)

### Backend
* django, djangorestframework
* simple jwt for user authentication,
* postgrsql/sqlite3 as database

## Installation

Make sure you have Python Installed in your System.

Install Virtual Env

```bash
virtualenv env
```
After Installing env navigate to env and activate it.

```bash
env\scripts\activate
```
After activation navigate to flight-booking-system and install requirements.

```bash
cd flight-booking-system
pip install -r requirements.txt
```
Now run these following commands

```bash
python manage.py makemigrations
python manage.py migrate flight_api
python manage.py migrate --run-syncdb
python manage.py runserver
```

Now you are ready to go for making request from frontend

if you want to make admin you have to be a superuser or you can send a request from postman to this URL

```bash
python manage.py createsuperuser
```
Url : HTTP://127.0.0.1:8000/flight-admin-register/ All the fields is required and password must be minimum of 6 characters
![image](https://github.com/bilal-patiwala/flight_booking_system/assets/95634055/4f100479-70a2-4187-9bcc-f29739942396)


## Changing Database

1) create .env File in your root directory

```bash
DB_NAME= 'postgres'
DB_USER= 'postgres'
DB_PASSWORD= 'your Password'
DB_HOST= 'Host Address'
DB_PORT= '5432'
```
2) add .env file into your .gitignore file
3) Run Makemigrations and migrate commands again

## License

[MIT](https://choosealicense.com/licenses/mit/)
