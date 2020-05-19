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

    return render_template("map_route.html", path_map=path_map, colormap=colormap)


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

    return render_template("map.html", time=height_map, colormap=colormap, name=name)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
