from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import requests
from datetime import datetime

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

# Fetch weather data from OpenWeatherMap API (this part remains the same)
def fetch_weather_data(api_key, city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    api_key = '72f08c0b39657cb8f3e52f34c851a4d7'  # Replace with your OpenWeather API key
    city = request.json['city']

    weather_data = fetch_weather_data(api_key, city)
    
    if weather_data:
        # print("ayush")
        # print("dsjfdksojffskdjfosdjflsdsjldgjlsdjfsdlkjfdslkfjdslkjldkjgldkljgldjgldjgldjg")
        first_forecast = weather_data['list'][0]
        temperature = first_forecast['main']['temp']
        humidity = first_forecast['main']['humidity'] / 1000
        precipitation = 0.017  # Replace with actual precipitation value if available
        wind_speed = first_forecast['wind']['speed'] * 3.66
        datetime_obj = datetime.strptime(first_forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        day_of_week = datetime_obj.weekday()
        holiday = 1 if day_of_week == 6 or day_of_week == 0 else 0

        # Prepare input data for prediction
        input_data = np.array([[temperature, humidity, precipitation, wind_speed, holiday]])
        input_data_scaled = scaler.transform(input_data)

        # Predict using the loaded model
        net_demand_prediction = model.predict(input_data_scaled)[0]

        return jsonify({
            'city': city,
            'temperature': temperature,
            'humidity': humidity,
            'precipitation': precipitation,
            'wind_speed': wind_speed,
            'holiday': holiday,
            'predicted_load': net_demand_prediction
        })
    else:
        # print("akash")
        return jsonify({'error': 'Failed to fetch weather data'})

if __name__ == '__main__':
    app.run(debug=True)
