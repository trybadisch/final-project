from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")  # from templates

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
