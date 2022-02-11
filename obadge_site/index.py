import flask
# importation de deux modules pour la barre de progression
# import alive_progress
# import time

app = flask.Flask(__name__)


class code_accueil:
    def __init__(self, code_HTML_principal):
        self.code_HTML_principal = code_HTML_principal

    @app.route("/")  # répertoire du site
    def Accueil():
        return flask.render_template("home.html")

    @app.route("/inscription")
    def Inscription():
        return flask.render_template("inscription.html")

    @app.route("/groupe")
    def Team():
        return flask.render_template("groupe.html")


html_code = code_accueil(code_HTML_principal=code_accueil)
print(html_code)
