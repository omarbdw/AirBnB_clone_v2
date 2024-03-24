#!/usr/bin/python3
""" Module that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Closes the current SQLAlchemy Session after each request.

    Args:
        exception (Exception): The exception that is raised.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """
    Renders a template that displays a list of states sorted by name.

    Returns:
        The rendered template with the sorted list of states.

    Raises:

    """

    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def cities_list(id):
    """
    Retrieve a list of cities for a given state ID.

    Args:
        id (str): The ID of the state.

    Returns:
        str: The rendered HTML template with the list of cities for the state.

    Raises:
        None

    """
    state = storage.get(State, id)
    if state is None:
        return render_template('9-not_found.html')
    else:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
