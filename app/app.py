from flask import Flask, render_template, request
from mpl_3d.plotly_3d import to_javascript
import time

app = Flask(__name__)


@app.route("/")
def main():
    app.jinja_env.cache = None
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def geo_map():
    size = request.form.get("geo")
    if not size.isdecimal():
        return "Bad input"
    size = int(size)
    if size < 1 or size > 100:
        return "Bad value"

    time = to_javascript((50, 5), size * 1000)
    return render_template("map.html", time=time)


if __name__ == "__main__":
    app.run(port=4300)
