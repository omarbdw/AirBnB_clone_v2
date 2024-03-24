#!/usr/bin/python3

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

""" Module that starts a Flask web application """

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Renders a template that displays a list of
    states and amenities sorted by name.

    Returns:
        The rendered template with the sorted list of states and amenities.

        Raises:
            None
    """
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda x: x.name)
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


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
