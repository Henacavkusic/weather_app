
# Weather app RESTful API

By using Open Weather Map as API provider this API simplifies their response for average user which means no geek stuff.
## Installation

First make sure you have installed `python` and `redis` on your system

[Python using anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) & [Redis](https://redis.io/docs/getting-started/installation/)

Clone the project

```
  git clone https://github.com/...
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

Create superuser

```
  python manage.py createsuperuser
```
You will be prompted to enter username, email (optional) and password


## Environment Variables

To run this project, you will need to create `env.py` inside weather_app directory and add the following environment variables to your `env.py` file

`OWM_API_KEY` - Open Weather Map

Example
``` OWM_API_KEY = "3967de3131f31fbbcc084d5c969e9020" ```


## API Reference

#### Create user (admin endpoint)

```
  POST curl -u superuserusername:superuserpassword http://127.0.0.1:8000/user/create/ -d "username=username" -d "password=password" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. |
| `password` | `string` | **Required**. |

#### Get current weather

```http
  GET curl -G -u username:password http://127.0.0.1:8000/weather/current/ -d "location=Sarajevo" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

#### Get forecast weather

```http
  GET curl -G -u username:password http://127.0.0.1:8000/weather/forecast/ -d "location=Sarajevo" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

#### Get historical weather

```http
  GET curl -G -u username:password http://127.0.0.1:8000/weather/history/ -d "location=Sarajevo" -d "date=2023-05-16" -d "country_code=BA" 
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `location` | `string` | **Required**. Location you want weather data for |
| `date` | `string` | **Required**. Date you want to get data for (i.e. '2023-05-16') |
| `state_code` | `string` | **Optional**. State code (only United States) |
| `country_code` | `string` | **Optional**. Country code |

## Documentation

[Documentation](https://...)

