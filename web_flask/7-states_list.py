#!/usr/bin/python3
""" Module that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Renders a template that displays a list of states sorted by name.

    Returns:
        The rendered template with the sorted list of states.
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Closes the current SQLAlchemy Session after each request.

    Args:
        exception (Exception): The exception that is raised.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
