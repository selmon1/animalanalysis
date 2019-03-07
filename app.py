from flask import Flask, render_template, flash, redirect, url_for, request

from model import AppModel
from view_header import Route
from presenter import Presenter


app = Flask(__name__)
app.secret_key = "secret"
model = AppModel(app)
presenter = Presenter(model)


def create_template(route):
    """
    Takes in a route to redirect to or render a template for

    """
    route_name = route.get_name()

    if route.is_redirect():
        return redirect(url_for(route_name))
    else:
        route_arg = route.get_args()
        if (route_arg == None):
            return render_template(route_name)
        return render_template(route_name, **(route_arg))


def present_flash(msg):
    """
    Passes a message at the end of the request if not null

    """
    if not (msg == None):
        flash(msg)


def render_view(view):
    """
    Flashes a message and renders a template for the given view 

    """
    present_flash(view.get_flash())
    return create_template(view.get_route())


# ~~~~~~~~~~ Routes ~~~~~~~~~~~~~~~~
@app.route('/')
def index():
    return render_template(presenter.index())


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        return render_view(presenter.analyze(request))
    else:
        return render_template(presenter.index())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
