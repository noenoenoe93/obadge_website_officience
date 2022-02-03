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
        return flask.render_template("index.html", nom_du_site = nom_du_site)

class heritage_de_code_accueil(code_accueil):
    def __init__(self, code_HTML_Accueil, code_HTML_herite):
        code_accueil.__init__(self, code_HTML_Accueil)
        self.code_HTML_herite = code_HTML_herite

    @app.route("/")
    def heritage():
        categories = {"Home": "Accueil", "Officience_groupe": "Officience Team", "collection_badges": "Badges Collection"}
        return flask.render_template("partie_construction.html", categories = categories)

html_code = heritage_de_code_accueil(heritage_de_code_accueil.heritage, code_accueil.Accueil)
print(html_code)