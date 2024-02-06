import requests
import os
import datetime as dt
# from requests.auth import HTTPBasicAuth

# basic = HTTPBasicAuth('Abdelrahman', 'Aboda948627@')

nutx_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_query = input("What exercise did you do?")

NUTX_ID = os.getenv("NUTX_ID")
NUTX_API = os.getenv("NUTX_API")

nutx_headers = {
    "x-app-id": NUTX_ID,
    "x-app-key": NUTX_API,
}

nutx_params = {
    "query": exercise_query,
    "gender": "male",
    "weight_kg": 69,
    "height_cm": 173,
    "age": 29
}

response = requests.post(url=nutx_endpoint, json=nutx_params, headers=nutx_headers)

the_workout = response.json()["exercises"][0]["name"]
duration = response.json()["exercises"][0]["duration_min"]
calories = response.json()["exercises"][0]["nf_calories"]

today = dt.datetime.today()
today_date = today.date()
formatted_date = today_date.strftime("%d/%m/%Y")
time_now = dt.datetime.now()
input_time = time_now.strftime("%X")

sheety_input_params = {
    "sheet1": {
        "date": formatted_date,
        "time": input_time,
        "exercise": the_workout.title(),
        "duration": duration,
        "calories": calories,
    }
}

SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PROJECTNAME = "myWorkouts"
SHEETY_SHEETNAME = "sheet1"

sheety_header = {
    "Authorization": "Bearer AAAAAAAALFWGK"
}

sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECTNAME}/{SHEETY_SHEETNAME}"

sheety_response_post = requests.post(url=sheety_endpoint, json=sheety_input_params, headers=sheety_header)

sheety_response_get = requests.get(url=sheety_endpoint, headers=sheety_header)


print(sheety_response_get.text)
