from flask import Flask, redirect, render_template, request, session
import requests
import datetime as dt

weather_api = "378b45b6e39bf0dfae6de624f1755760"
news_api = "f427c0f6059648f5a0a85f8cda8a6cd8"

app = Flask(__name__)

@app.route("/")
def index():
	# ip = request.remote_addr
	ip = "92.57.105.25"
	response = requests.get(url=f'https://ipapi.co/{ip}/json/')
	data = response.json()

	weather_params = {
		"lat": data["latitude"], "lon": data["longitude"],
		"appid": "69f04e4613056b159c2761a9d9e664d2"  # change API key
	}
	response = requests.get(url='https://api.openweathermap.org/data/2.5/weather', params=weather_params)
	weather = response.json()["weather"][0]["description"].title()

	news_params = {
		"language": "en",
		"sortBy": "popularity",
		"apiKey": news_api
	}
	response = requests.get(url='http://newsapi.org/v2/top-headlines', params=news_params)
	news = response.json()["articles"][:3]

	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("index.html", ip=ip, data=data, weather=weather, news=news, time=time)

@app.route("/data")
def data():
	return render_template("data.html")

@app.route("/terminal")
def terminal():
	return render_template("terminal.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")


@app.route("/about")
def about():
	return render_template("about.html")
