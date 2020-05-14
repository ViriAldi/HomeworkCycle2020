from flask import Flask, render_template, request
from mpl_3d.plotly_3d import save_csv


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def geo_map():
    size = request.form.get("geo")
    if not size.isdecimal():
        return "Bad input"
    size = int(size)
    if size < 1 or size > 40:
        return "Bad value"

    save_csv((50, 5), size * 1000)
    return render_template("map.html")


app.run(debug=True)
