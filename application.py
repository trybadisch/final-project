from flask import Flask, render_template, request, redirect
import requests
import sqlite3
import datetime as dt
import os

WEATHER_API = os.getenv('WEATHER_API')
NEWS_API = os.getenv('NEWS_API')
IP_API = os.getenv('IP_API')

DATA = None
MESSAGES = None
THEME = "green"
RUNNING = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

IP = None
ERROR = None

def get_info(forced=False):
	global DATA, ERROR, IP
	if not DATA or not forced:
		if not IP:
			ip = requests.get(url='https://api64.ipify.org?format=json').json()['ip']
		else:
			ip = IP

		api_params = {
			"access_key": IP_API,
			"hostname": 1,
		}
		response = requests.get(url=f'http://api.ipapi.com/api/{ip}', params=api_params)
		data = response.json()

		try:
			if data["error"]:
				print("[+]", data)
				IP = None
				ERROR = data["reason"]
				return
			else:
				ERROR = None
		except KeyError:
			pass

		try:
			weather_params = {
				"lat": data["latitude"], "lon": data["longitude"],
				"appid": WEATHER_API
			}
			response = requests.get(url='https://api.openweathermap.org/data/2.5/weather', params=weather_params)
			weather = response.json()["weather"][0]["description"].title()
		except KeyError:
			weather = "No data available"

		news_params = {
			"language": "en",
			"sortBy": "popularity",
			"apiKey": NEWS_API
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

	global IP
	if request.method == "POST":
		message=request.form.get("message")
		terminal=request.form.get("command")
		if message:
			new_message(message)
			check_msg()
		if terminal:
			if "color" in terminal or "theme" in terminal:
				theme_change(terminal)
			elif "check" in terminal:
				IP = terminal.split()[1]
				get_info(forced=True)
				return redirect("/")

	return render_template("index.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, messages=MESSAGES, theme=THEME, runtime=RUNNING)

@app.route("/terminal", methods=["GET", "POST"])
def terminal():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	global IP
	if request.method == "POST":
		terminal=request.form.get("command")
		if terminal:
			if "color" in terminal or "theme" in terminal:
				theme_change(terminal)
			elif "check" in terminal:
				IP = terminal.split()[1]
				get_info(forced=True)
				return redirect("/")

	return render_template("terminal.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME, runtime=RUNNING)

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

	return render_template("dashboard.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, messages=MESSAGES, theme=THEME, runtime=RUNNING)

@app.route("/map")
def map():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("map.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME, runtime=RUNNING)

@app.route("/about")
def about():
	get_info()
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("about.html", ip=DATA['ip'], data=DATA['data'], weather=DATA['weather'], news=DATA['news'], time=time, theme=THEME, runtime=RUNNING)

@app.route("/error")
def error():
	time = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

	return render_template("error.html", reason=ERROR, theme=THEME, runtime=RUNNING)
