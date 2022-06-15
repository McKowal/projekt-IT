# from flask import Flask
import matplotlib.pyplot as plt
import numpy as np
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


# app = Flask(__name__)

# @app.route("/")

function_name = 'sin(x)'
point = 4
plot = make_plot(function_name, point)
plot.show()
