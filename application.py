from flask import Flask, redirect, render_template, request, session
import requests
import sqlite3
import datetime as dt

weather_api = "378b45b6e39bf0dfae6de624f1755760"
news_api = "f427c0f6059648f5a0a85f8cda8a6cd8"

DATA = None
MESSAGES = None
THEME = "green"

def get_info():
	global DATA
	if not DATA:
		# ip = request.remote_addr
		ip = "92.57.105.25"
		response = requests.get(url=f'https://ipapi.co/{ip}/json/')
		data = response.json()

		weather_params = {
			"lat": data["latitude"], "lon": data["longitude"],
			"appid": weather_api
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

		DATA = {
		'ip': ip,
		'data': data,
		'weather': weather,
		'news': news,
		}
		return DATA
	return

def check_db():
	connection = sqlite3.connect("database.db")
	cursor = connection.execute("SELECT ip FROM visitors WHERE ip = ?", (DATA['ip'],))
	check = cursor.fetchone()
	if check is None:
		connection.execute("INSERT INTO visitors (ip, lat, lon) VALUES (?, ?, ?)", (DATA['ip'], DATA['data']['latitude'], DATA['data']['longitude']))
		connection.commit()
	connection.close()

def check_msg():
	global MESSAGES
	connection = sqlite3.connect("database.db")
	cursor = connection.execute("SELECT * FROM messages")
	messages = cursor.fetchall()
	connection.close()
	MESSAGES = messages

def new_message(message):
	connection = sqlite3.connect("database.db")
	connection.execute("INSERT INTO messages (ip, message) VALUES (?, ?)", (DATA['ip'], message))
	connection.commit()
	connection.close()

def theme_change(terminal):
	global THEME
	if terminal == "color-green":
		THEME = "green"
	elif terminal == "color-red":
		THEME = "red"
	elif terminal == "color-blue":
		THEME = "blue"
	elif terminal == "theme-light":
		THEME = "light"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	get_info()
	check_db()
	check_msg()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	if request.method == "POST":
		message=request.form.get("message")
		terminal=request.form.get("command")
		if message:
			new_message(message)
			check_msg()
		if terminal:
			theme_change(terminal)

	return render_template("index.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, messages=MESSAGES, theme=THEME)

@app.route("/terminal", methods=["GET", "POST"])
def terminal():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	if request.method == "POST":
		terminal=request.form.get("command")
		if terminal:
			theme_change(terminal)

	return render_template("terminal.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	get_info()
	check_msg()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	if request.method == "POST":
		message=request.form.get("message")
		if message:
			new_message(message)
			check_msg()

	return render_template("dashboard.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, messages=MESSAGES, theme=THEME)

@app.route("/map")
def map():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("map.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME)

@app.route("/about")
def about():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("about.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME)
