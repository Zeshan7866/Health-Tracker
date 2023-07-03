import requests
import gspread
import datetime


sa = gspread.service_account(filename="health-tracker-376817-ef524ca964bd.json")
sh = sa.open("My_Workouts")
work_sheet = sh.worksheet("Sheet1")

nutrition_api_app_id = "29b3abf1"
nutrition_api_app_key = "e02d719e6abec4ebe8e3ea69b4c6c63a"
nutrition_end_point = "https://trackapi.nutritionix.com/v2/natural/exercise"


activity_input = input("Tell me what exercises you did: ")
data = {
 "query": activity_input,
 "gender": "male",
 "weight_kg": 67,
 "height_cm": 167.64,
 "age": 21
}

headers = {
  "x-app-id": nutrition_api_app_id,
  "x-app-key": nutrition_api_app_key,
}

dt = datetime.datetime.now()
date = dt.strftime("%Y-%m-%d")
time = dt.strftime("%H:%M:%S")

response_1 = requests.post(url=nutrition_end_point, json=data, headers=headers)
activity_data = response_1.json()

sheet_inputs = {'exercises': [{"date": date, "time": time, 'name': exercise['name'],
                               'duration_min': exercise['duration_min'],
                               'nf_calories': exercise['nf_calories']} for exercise in activity_data['exercises']]}
data = sheet_inputs["exercises"]

for x in range(len(data)):
    d = data[x]
    value_list = list(d.values())
    work_sheet.append_row(values=value_list)
