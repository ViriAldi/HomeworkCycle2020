from flask import Flask, render_template, request
from mpl_3d.plotly_3d import to_javascript, make_path
from geocoder.geocoder import locate, decode
from math import floor
import os

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/choosing_<string:name>")
def choosing(name):
    return render_template("choosing.html", way=name)


@app.route("/making_<string:name>")
def making_path(name):
    path = f"making_{name}.html"
    if path not in os.listdir("templates"):
        return "No such page"
    return render_template(path)


@app.route("/map_route", methods=["POST"])
def map_route():
    name1 = name2 = ""
    if request.form.get("name1", "") != "":
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        try:
            coord1 = locate(name1)
            coord2 = locate(name2)
        except AttributeError:
            return "No such location!"
    else:
        lat1 = float(request.form.get("lat1"))
        lat2 = float(request.form.get("lat2"))
        lon1 = float(request.form.get("lon1"))
        lon2 = float(request.form.get("lon2"))
        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)

    if floor(coord1[0]) != floor(coord2[0]) or floor(coord1[1]) != floor(coord2[1]):
        return "Different squares"
    colormap = request.form.get("color")

    try:
        path_map = make_path(coord1, coord2)
    except FileNotFoundError:
        return "No data"

    coord = ((coord1[0] + coord1[0]) / 2, (coord1[1] + coord1[1]) / 2)

    country, address = decode(coord)
    address = " ".join("".join(str(address).split(",")[:2]).split()[:6])
    size = 2 * int(max(0.75 * max(abs(coord2[0] - coord1[0]), abs(coord2[1] - coord1[1])) * 120, 5))

    return render_template("map_route.html", path_map=path_map, colormap=colormap, name=f"{name1.capitalize()} - {name2.capitalize()}", lat=coord[0], lon=coord[1], country=country, address=address, size=size)


@app.route("/map", methods=["POST"])
def geo_map():
    name = ""
    if request.form.get("name", "") != "":
        name = request.form.get("name")
        try:
            coord = locate(request.form.get("name"))
        except AttributeError:
            return "No such location!"
    else:
        lat = float(request.form.get("geo1"))
        long = float(request.form.get("geo2"))
        coord = (lat, long)

    size = request.form.get("size")
    if not size.isdecimal():
        return "Bad input"
    size = int(size)
    if size < 1:
        return "Bad value"

    colormap = request.form.get("color")

    try:
        height_map = to_javascript(coord, size * 1000)
    except FileNotFoundError:
        return "No data"

    country, address = decode(coord)
    address = " ".join("".join(str(address).split(",")[:2]).split()[:6])

    return render_template("map.html", time=height_map, colormap=colormap, name=name.capitalize(), lat=coord[0], lon=coord[1], country=country, address=address, size=2*size)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
