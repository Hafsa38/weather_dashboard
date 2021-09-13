import requests
import configparser
import os
from flask import Flask, render_template,request

app =Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    city_name = request.form['cityName']

    api_key= get_api_key()
    data = get_weather_results(city_name,api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    weather = data["weather"][0]["description"]
    pressure = "{0:.2f}".format(data["main"]["pressure"])
    humidity = "{0:.2f}".format(data["main"]["humidity"])
    location = data["name"]

    return render_template('results.html',location = location,temp=temp,weather=weather,
                         pressure=pressure,humidity=humidity)

def get_api_key():
    config = configparser.ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'config.ini'))
    return config['openweathermap']['api']

def get_weather_results(city_name,api_key):
    api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name,api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()

