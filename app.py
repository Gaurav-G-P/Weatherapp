from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = '8a5d7c5251afc477cd925e0a63a41a2a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    weather_data = fetch_weather_data(city)
    if weather_data:
        return render_template('index.html', weather=weather_data)
    else:
        return render_template('index.html', error="City not found or invalid.")


def fetch_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        city_name = data['name']
        country = data['sys']['country']

        weather_info = {
            'city': city_name,
            'country': country,
            'temperature': main['temp'],
            'description': weather['description'],
            'humidity': main['humidity'],
            'wind_speed': wind['speed'],
        }
        return weather_info
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
