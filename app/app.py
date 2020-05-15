from flask import Flask, render_template, request
from mpl_3d.plotly_3d import to_javascript, make_path
from geocoder.geocoder import locate

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/making_map")
def making_map():
    return render_template("making_map_coordinates.html")


@app.route("/making_path")
def making_path():
    return render_template("making_path_coordinates.html")


@app.route("/map_route", methods=["POST"])
def map_route():
    lat1 = float(request.form.get("lat1"))
    lat2 = float(request.form.get("lat2"))
    lon1 = float(request.form.get("lon1"))
    lon2 = float(request.form.get("lon2"))

    path_map = make_path((50, 5), (lat1, lon1), (lat2, lon2))
    return render_template("map_route.html", path_map=path_map)


@app.route("/map", methods=["POST"])
def geo_map():
    size = request.form.get("size")
    if not size.isdecimal():
        return "Bad input"
    size = int(size)
    if size < 1 or size > 100:
        return "Bad value"

    colormap = request.form.get("color")
    lat = float(request.form.get("geo1"))
    long = float(request.form.get("geo2"))

    height_map = to_javascript((50, 5), (lat, long), size * 1000)
    return render_template("map.html", time=height_map, colormap=colormap)


if __name__ == "__main__":
    app.run(port=4300, debug=True)
