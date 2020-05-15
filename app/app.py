from flask import Flask, render_template, request
from mpl_3d.plotly_3d import to_javascript, make_path
from geocoder.geocoder import locate

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/making_map_geocoder")
def making_map_geocoder():
    return render_template("making_map_geocoder.html")


@app.route("/making_path_geocoder")
def making_path_geocoder():
    return render_template("making_path_geocoder.html")


@app.route("/choosing_<string:name>")
def choosing(name):
    return render_template("choosing.html", way=name)


@app.route("/making_map_coordinates")
def making_map():
    return render_template("making_map_coordinates.html")


@app.route("/making_path_coordinates")
def making_path():
    return render_template("making_path_coordinates.html")


@app.route("/map_route", methods=["POST"])
def map_route():
    if request.form.get("name1", "") != "":
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        coord1 = locate(name1)
        coord2 = locate(name2)
    else:
        lat1 = float(request.form.get("lat1"))
        lat2 = float(request.form.get("lat2"))
        lon1 = float(request.form.get("lon1"))
        lon2 = float(request.form.get("lon2"))
        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)

    if abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1]) > 1:
        return f"too long: Point1({coord1}), Point2({coord2})"

    path_map = make_path((50, 5), coord1, coord2)
    return render_template("map_route.html", path_map=path_map)


@app.route("/map", methods=["POST"])
def geo_map():
    if request.form.get("name", "") != "":
        coord = locate(request.form.get("name"))
    else:
        lat = float(request.form.get("geo1"))
        long = float(request.form.get("geo2"))
        coord = (lat, long)

    size = request.form.get("size")
    if not size.isdecimal():
        return "Bad input"
    size = int(size)
    if size < 1 or size > 100:
        return "Bad value"

    colormap = request.form.get("color")

    height_map = to_javascript((50, 5), coord, size * 1000)
    return render_template("map.html", time=height_map, colormap=colormap)


if __name__ == "__main__":
    app.run(port=4300, debug=True)
