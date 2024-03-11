# NLP Workouts Tracker On Google Sheets

---

- On this tool you log your workouts by answering the below question with a normal sentence like:
```
What exercise did you do today?
```
> I ran for 5 kilometers.
- Using Natural Language Processing provided by NutritionX API, it extracts the type
of workout, its estimated duration and calories burnt.
- It also saves this data to a Google sheet using Sheety API.
![workouts screenshot](https://github.com/Abdelrahman-Elsaudy/Habit-Tracker-Using-Pixela/assets/158151388/14d7baa9-1f6f-45ad-b34b-249d41604953)
---
## Skills Practiced:

---

- Making API `get` requests to NutritionX NLP to gain insights about the input workout.
- `JSON` data manipulation to extract the desired info for the next API requests for Sheety API.
- Using `datetime` module to get info about the date and time of the workouts.
- Making API `post` and `get` requests to Sheety API to add and retrieve data on Google sheets.
- Using `Pandas` module to save the personal features data to a csv file when the user uses the tool for 
the first time and read this data for future workout logs.

---

## Prerequisites:

---

- Signing up to [NutritionX](https://developer.nutritionix.com/login) to get a free ID and API key.
- Signing up to [Sheety](https://sheety.co/) and connecting your Google account to it.
- Creating a token on Sheety to authorize the access to your sheet.
- Creating a Google sheet on your account and naming it to use it later for reading and writing the workouts data from and to it.

---
## How This Tool Works:

**1. Personalization**

- This part wasn't on the original project from _100 Days of Code_ Course on Udemy but I added it to give the tool 
a personalization feature.
- I used `try`, `except` and `else` method to account for the first time the user opens the tool.
- The tool starts by asking you about your gender, weight, height and age to be passed as parameters to NutritionX API
as written in the [documentation](https://docx.syndigo.com/developers/docs/natural-language-for-exercise).

```
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
}
```
- If it's your first time, this data will be saved on a csv file called "personal_features.csv" and will be used
for future workouts logs.
---

**2. Using NLP to Get Workout Data**

- After obtaining NutritionX ID, API and the provided personal info, I make a get request to its endpoint with those
parameters to get the workout data as JSON format.
- Then I put the response on [JSON viewer](https://jsonviewer.stack.hu/) to make it easier to read.
- Then I assign the workout data to variables to prepare it for the next API parameters of Sheety.
```
response = requests.post(url=nutx_endpoint, json=nutx_params, headers=nutx_headers)
response.raise_for_status()

the_workout = response.json()["exercises"][0]["name"]
duration = response.json()["exercises"][0]["duration_min"]
calories = response.json()["exercises"][0]["nf_calories"]
```

---

**3. Saving Workout Data to Google Sheets**
- Here I use the `datetime` module and `strftime` method to get the date and time of the workout
in the required format, we can do this with datetime [documentation](https://www.w3schools.com/python/python_datetime.asp).
- After preparing Sheety parameters I use `post ` request to post the workout details on my Google sheet.
```
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
```

---

## User Tips:
- When dealing with Sheety, I recommend opening Sheety [documentation](https://sheety.co/docs/requests.html) alongside with your dashboard to make it easier to prepare
the required parameters and make the desired requests.
- You can make requests to edit or delete a row on your Google sheet using Sheety, this is also found on the [documentation](https://sheety.co/docs/requests.html).
- I use `print(sheety_response_get.text)` to know the status of the request whether it was successful or not.

---
_Credits to: 100-Days of Code Course on Udemy._