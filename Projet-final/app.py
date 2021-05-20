import requests
import configparser
from flask import Flask, render_template, request

api_key="8803bc343612b046733be88b6fc22f71"

app = Flask(__name__,template_folder='templates')

@app.route('/')
def weather_dashboard():
    return render_template('index.html')


@app.route('/meteo', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    code = data["zipCode"]

    return render_template('meteo.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather, code=code)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('API.txt')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()





if __name__ == '__main__':
    app.run(debug=True)
