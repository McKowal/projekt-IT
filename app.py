from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
from numpy import *
matplotlib.use('Agg')


def calculate_slope(function, x):
    h = 0.001
    return (function_value(function, x + h) - (function_value(function, x - h))) / (2 * h)


def function_value(name, x):
    try:
        name = eval(name)
    except NameError:
        return []
    return name


def make_plot(name, x):
    step = 0.001
    x_range = arange(x - 5, x + 5, step)
    plt.clf()
    value = function_value(name, x_range)
    if len(value) == 0:
        return
    plt.plot(x_range, value, label=name)
    slope = calculate_slope(name, x)
    tangent_x_range = arange(x - 1, x + 1, step)
    plt.plot(tangent_x_range, slope * (tangent_x_range - x) + function_value(name, x),
             label='{} * x + {}'.format(round(slope, 2), round(function_value(name, x) - slope * x, 2)))
    plt.title(name)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    url = base64.b64encode(img.getvalue()).decode()
    return 'data:image/png;base64,{}'.format(url)


app = Flask(__name__)
app.secret_key = "a"


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/dane", methods=["POST", "GET"])
def dane():
    return render_template("dane.html")


@app.route("/styczna", methods=["POST", "GET"])
def tangent_line():
    return render_template("styczna.html")


@app.route("/plot", methods=["POST", "GET"])
def plot():
    function = str(request.form['function'])
    try:
        point = float(request.form['point'])
    except ValueError:
        return render_template("styczna.html")
    p = make_plot(function, point)
    if not p:
        return render_template("styczna.html")
    plotting = True
    return render_template("styczna.html", plot=p, plotting=plotting)
