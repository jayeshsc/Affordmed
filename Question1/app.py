from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Endpoint to fetch train data
API_ENDPOINT = "http://20.244.56.144/train/trains"
AUTH_TOKEN = "eyJhbGci0iJIUzI1NiIsIn5cCI6IkpXVCJ9.eyJleHAi0jE20DI2MjkyNjQsImNvbXBhbn10YW11IjoiVHJhaw4gQ2VudHJhbCIsImNsaWVudElEIjoiYjQ2MTE4ZjAtZm]kZS00YjE2LWEYjEtNmF1NmFkNzE4YjI3In0.v93QcxrZHWDTnTwmO-6t toTGI4C64Grhn7rIJDC8fy8"  

def fetch_real_time_train_data():
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def filter_and_sort_trains(trains_data):
    now = datetime.now()
    next_12_hours = now + timedelta(hours=12)
    filtered_trains = []

    for train in trains_data:
        departure_time = datetime.strptime(train['departure_time'], "%Y-%m-%d %H:%M:%S")

        # Filter out trains departing in the next 30 minutes
        if (departure_time - now).total_seconds() >= 30 * 60:
            # Filter trains departing in the next 12 hours
            if departure_time <= next_12_hours:
                filtered_trains.append(train)

    # Sort trains based on criteria: price (ascending), availability (descending), departure time (descending)
    sorted_trains = sorted(
        filtered_trains,
        key=lambda train: (train['sleeper_price'] + train['ac_price'], -train['sleeper_availability'], -departure_time.timestamp())
    )

    return sorted_trains

@app.route('/trains', methods=['GET'])
def get_trains():
   
    trains_data = fetch_real_time_train_data()

   
    sorted_trains = filter_and_sort_trains(trains_data)

   
    return jsonify({'trains': sorted_trains})

if __name__ == '__main__':
    app.run(debug=True)
