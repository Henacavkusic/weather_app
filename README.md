# Weather app RESTful API

By using Open Weather Map as API provider this API simplifies their response for average user which means no geek stuff.

## Installation

First make sure you have installed `python` and `redis` on your system

[Python using anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) & [Redis](https://redis.io/docs/getting-started/installation/)

Clone the project

```
  git clone https://github.com/Henacavkusic/weather_app.git
```

Go to the project directory

```
  cd my-project
```

Install dependencies

```
  pip install -r requirements.txt
```

Create database

```
  python manage.py migrate
```

Create superuser (admin)

```
  python manage.py createsuperuser
```
You will be prompted to enter username, email (optional) and password

Run server
```
  python manage.py runserver
```

## Environment Variables

To run this project, you will need to create `env.py` inside weather_app directory and add the following environment variables to your `env.py` file

`OWM_API_KEY` - Open Weather Map API key

Example
``` OWM_API_KEY = "3967de3131f31fbbcc084d5c969e9020" ```

## API Reference

#### Import Postman collection

[Weather App Collection](https://api.postman.com/collections/6892014-0a6e0552-e425-4c1b-8837-96c9fad4635d?access_key=PMAT-01H0BN34M3KRVXW9Z00KC1DR93)

#### Create user (admin endpoint)

```
  POST: curl -u admin:adminpassword http://127.0.0.1:8000/user/create/ -d "username=username" -d "password=password" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. |
| `password` | `string` | **Required**. |

#### Get current weather

```
  GET: curl -G -u username:password http://127.0.0.1:8000/weather/current/ -d "location=Sarajevo" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

#### Get forecast weather

```
  GET: curl -G -u username:password http://127.0.0.1:8000/weather/forecast/ -d "location=Sarajevo" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

#### Get historical weather

```
  GET: curl -G -u username:password http://127.0.0.1:8000/weather/history/ -d "location=Sarajevo" -d "date=2023-05-16" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `date` | `string` | **Required**. Date you want to get data for (i.e. '2023-05-16') |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

## Documentation

[Documentation](https://...)

