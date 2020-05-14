from flask import Flask, render_template
from mpl_3d.plotly_3d import save_csv


app = Flask(__name__)


@app.route("/")
def main():
    save_csv((50, 5), 30000)
    return render_template("index.html")


app.run(debug=True)
