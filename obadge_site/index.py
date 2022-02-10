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
        categories = {"Home": "Accueil", "Officience_groupe": "Officience Team", "Collection_badges": "Badges Collection"}
        return flask.render_template("index.html", nom_du_site = nom_du_site, categories = categories)

class heritage_de_code_accueil(code_accueil):
    def __init__(self, code_HTML_principale, code_HTML_herite):
        code_accueil.__init__(self, code_HTML_principale)
        self.code_HTML_herite = code_HTML_herite

    @app.route("/static")
    def login():
        login = {"Authentification": "Login"}
        return flask.render_template("login.html", login = login)

    @app.route("/static")
    def Inscription():
        inscription = {"Authentification": "Sign Up"}
        return flask.render_template("inscription.html", inscription = inscription)

html_code = code_accueil(heritage_de_code_accueil)
print(html_code)