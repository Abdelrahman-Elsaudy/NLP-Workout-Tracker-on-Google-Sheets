import requests
import datetime as dt
import pandas


# ------------------------------------------- PERSONAL FEATURES ------------------------------------------- #


try:
    data = pandas.read_csv("personal_features.csv")
except FileNotFoundError:
    gender = input("Enter your gender: ")
    weight = input("Enter your weight in kg: ")
    height = input("Enter your height in cm: ")
    age = input("Enter your age: ")
    data = {
        "gender": [gender],
        "weight": [weight],
        "height": [height],
        "age": [age]
    }
    df = pandas.DataFrame(data)
    df.to_csv("personal_features.csv")
else:
    data_dict = data.to_dict()
    gender = data_dict["gender"][0]
    weight = data_dict["weight"][0]
    height = data_dict["height"][0]
    age = data_dict["age"][0]


# ------------------------------------------- NUTRITIONX API ------------------------------------------- #


with open("api.txt") as file:
    content = file.readlines()
    NUTX_ID = content[1].replace("\n", "")
    NUTX_API = content[3].replace("\n", "")

nutx_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

nutx_headers = {
    "x-app-id": NUTX_ID,
    "x-app-key": NUTX_API
}

exercise_query = input("What exercise did you do today? ")

nutx_params = {
    "query": exercise_query,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age
}

response = requests.post(url=nutx_endpoint, json=nutx_params, headers=nutx_headers)
response.raise_for_status()

the_workout = response.json()["exercises"][0]["name"]
duration = response.json()["exercises"][0]["duration_min"]
calories = response.json()["exercises"][0]["nf_calories"]


# ------------------------------------------- SHEETY API ------------------------------------------- #


with open("api.txt") as file:
    SHEETY_USERNAME = content[5].replace("\n", "")
    SHEETY_API = content[7].replace("\n", "")

today = dt.datetime.today()
today_date = today.date()
formatted_date = today_date.strftime("%d/%m/%Y")
time_now = dt.datetime.now()
input_time = time_now.strftime("%X")

SHEETY_PROJECTNAME = "myWorkouts"     # camelCase.
SHEETY_SHEETNAME = "sheet1"

sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECTNAME}/{SHEETY_SHEETNAME}"

sheety_header = {
    "Authorization": SHEETY_API
}

sheety_input_params = {
    SHEETY_SHEETNAME: {
        "date": formatted_date,
        "time": input_time,
        "exercise": the_workout.title(),
        "duration": duration,
        "calories": calories,
    }
}

sheety_response_post = requests.post(url=sheety_endpoint, json=sheety_input_params, headers=sheety_header)
sheety_response_post.raise_for_status()

sheety_response_get = requests.get(url=sheety_endpoint, headers=sheety_header)
sheety_response_get.raise_for_status()

print(sheety_response_get.text)
