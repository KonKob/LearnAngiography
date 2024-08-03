from flask import Flask
import solara.server.flask
from solara_app import Page

app = Flask(__name__)
app.register_blueprint(solara.server.flask.blueprint)

@app.route("/")
def load_page():
    return Page()

if __name__ == '__main__':  # Script executed directly?
    app.run()