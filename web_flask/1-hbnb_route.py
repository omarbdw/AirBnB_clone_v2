#!/usr/bin/python3
""" Module that starts a Flask web application """
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Returns a greeting message.

    Returns:
            str: The greeting message 'Hello HBNB!'.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Returns a message.

    Returns:
            str: The message 'HBNB'.
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
