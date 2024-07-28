from flask import Flask
import solara.server.flask
from solara_app import Page

app = Flask(__name__)
app.register_blueprint(solara.server.flask.blueprint, url_prefix="/main/")

@app.route("/")
def load_page():
    Page()