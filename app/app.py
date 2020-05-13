from flask import Flask, render_template
from mpl_3d.visualize import save_vis


app = Flask("application")


@app.route("/")
def main():
    vis = save_vis("..geofiles/swizerland.tiff", geo_corner=(50, 5))
    return render_template("index.html", value=vis)


if __name__ == "__main__":
    app.run()

