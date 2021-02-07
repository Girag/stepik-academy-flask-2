from flask import Flask, render_template, abort
import data

app = Flask(__name__)


@app.errorhandler(404)
@app.errorhandler(KeyError)
def render_not_found(_):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!", 404


@app.route("/")
def render_main():
    return render_template("index.html", tours=data.tours,
                           title=data.title,
                           subtitle=data.subtitle,
                           description=data.description,
                           departures=data.departures)


@app.route("/departures/<departure>/")
def render_departures(departure):
    tours = dict(filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    if tours:
        return render_template("departure.html", departure=departure,
                               title=data.title,
                               departures=data.departures,
                               tours=tours)
    else:
        abort(404)


@app.route("/tours/<int:id>/")
def render_tours(id):
    return render_template("tour.html", tour=data.tours[id],
                           title=data.title,
                           departures=data.departures)


if __name__ == '__main__':
    app.run()
