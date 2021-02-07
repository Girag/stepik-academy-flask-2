from flask import Flask, render_template, abort
import data

app = Flask(__name__)


@app.errorhandler(404)
def render_not_found(_):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!", 404


@app.route("/")
def render_main():
    tours = {k: v for k, v in data.tours.items() if k in range(1, 7)}
    return render_template("index.html", tours=tours,
                           title=data.title,
                           subtitle=data.subtitle,
                           description=data.description,
                           departures=data.departures)


@app.route("/departures/<departure>/")
def render_departures(departure):
    tours = dict(filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    price_min, price_max, nights_min, nights_max = float("inf"), float("-inf"), float("inf"), float("-inf")
    for tour in tours.values():
        if tour["price"] < price_min:
            price_min = tour["price"]
        if tour["price"] > price_max:
            price_max = tour["price"]
        if tour["nights"] < nights_min:
            nights_min = tour["nights"]
        if tour["nights"] > nights_max:
            nights_max = tour["nights"]

    if tours:
        return render_template("departure.html", departure=departure,
                               title=data.title,
                               departures=data.departures,
                               tours=tours,
                               price_min=price_min,
                               price_max=price_max,
                               nights_min=nights_min,
                               nights_max=nights_max)
    abort(404)


@app.route("/tours/<int:id>/")
def render_tours(id):
    if id in data.tours:
        return render_template("tour.html", tour=data.tours[id],
                               title=data.title,
                               departures=data.departures)
    abort(404)


if __name__ == '__main__':
    app.run()
