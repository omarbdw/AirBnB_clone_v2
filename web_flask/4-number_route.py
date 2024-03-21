#!/usr/bin/python3
""" Module that starts a Flask web application """
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Returns the string "HBNB".
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Returns a string with 'C' followed by the text parameter,
    where underscores are replaced with spaces.

    Args:
            text (str): The text parameter to be included in the response.

    Returns:
            str: A string with 'C' followed by the modified text.
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    """
    Returns a string with 'Python' followed by the text parameter,
    where underscores are replaced with spaces.

    Args:
            text (str): The text parameter to be included in the response.
                         Default value is 'is cool'.

    Returns:
            str: A string with 'Python' followed by the modified text.
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """
    Returns a string indicating whether n is a number or not.

    Args:
            n (int): The number to be checked.

    Returns:
            str: A string indicating whether n is a number or not.
    """
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
