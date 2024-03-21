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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
