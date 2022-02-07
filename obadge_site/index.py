from cmath import log
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
    # login du site
        login = {"Authentification": "Login"}
        return flask.render_template("index.html", nom_du_site = nom_du_site, categories = categories, login = login)

html_code = code_accueil(code_accueil.Accueil)
print(html_code)

'''
class heritage_de_code_accueil(code_accueil):
    def __init__(self, code_HTML_Accueil, code_HTML_herite):
        code_accueil.__init__(self, code_HTML_Accueil)
        self.code_HTML_herite = code_HTML_herite

    @app.route("/")
    def heritage():
        categories = {"Home": "Accueil", "Officience_groupe": "Officience Team", "Collection_badges": "Badges Collection"} # appel de ce dictionnaire dans "partie_construction.html"
        return flask.render_template("partie_construction.html", categories = categories)
'''