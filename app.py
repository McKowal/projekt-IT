from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from numpy import sin


def calculate_slope(function, x):
    h = 0.001
    return (function_value(function, x + h) - (function_value(function, x - h))) / (2 * h)


def function_value(name, x):
    return eval(name)


def make_plot(name, x):
    step = 0.001
    x_range = np.arange(x - 5, x + 5, step)
    plt.plot(x_range, function_value(name, x_range), label=name)
    slope = calculate_slope(name, x)
    tangent_x_range = np.arange(x - 1, x + 1, step)
    plt.plot(tangent_x_range, slope * (tangent_x_range - x) + function_value(name, x),
             label='{} * x + {}'.format(np.round(slope, 2), np.round(function_value(name, x) - slope * x, 2)))
    plt.title(name)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    return plt


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
    img = io.BytesIO()
    function = str(request.form['function'])
    point = float(request.form['point'])
    p = make_plot(function, point)
    p.savefig(img, format='png')
    img.seek(0)
    url = base64.b64encode(img.getvalue()).decode()
    p = 'data:image/png;base64,{}'.format(url)
    plotting = True
    return render_template("styczna.html", plot=p, plotting=plotting)
