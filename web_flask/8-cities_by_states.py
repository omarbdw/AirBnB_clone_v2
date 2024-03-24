#!/usr/bin/python3
""" Module that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models import *
app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Display a webpage with a list of cities grouped by states.

    Returns:
        The rendered template '8-cities_by_states.html'
        with the states variable.
    """
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
