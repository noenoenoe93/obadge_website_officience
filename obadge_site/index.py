import flask
# importation de deux modules pour la barre de progression
# import alive_progress 
# import time

app = flask.Flask(__name__)

class code_accueil:
    def __init__(self, code_HTML_principal):
        self.code_HTML_principal = code_HTML_principal

    @app.route("/") # répertoire du site
    def Accueil():
    # titre du site
        nom_du_site = {"nomsite": "Openbadge"}
    # categories du site
        login = {"Authentification": "Login"}
        inscription = {"Authentification": "Sign Up"}
        categories = {"Home": "Accueil", "Officience_groupe": "Officience Team", "Collection_badges": "Badges Collection"}
        return flask.render_template("index.html", nom_du_site = nom_du_site, categories = categories, login = login, inscription = inscription)

    @app.route("/login")
    def Login():
    # login du site
        return flask.render_template("login.html")

    @app.route("/inscription")
    def Inscription():
    # inscription du site
        return flask.render_template("inscription.html")

html_code = code_accueil(code_HTML_principal = code_accueil)
print(html_code)