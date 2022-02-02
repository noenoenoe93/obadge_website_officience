from datetime import datetime
import flask
# importation de deux modules pour la barre de progression
# import alive_progress 
# import time

app = flask.Flask(__name__)

class code:
    def __init__(self, code_HTML):
        self.code_HTML = code_HTML

@app.route("/") # répertoire du site
def code_html_principale():
    # titre du site
    nom_du_site = {"nomsite": "Openbadge"}
    # menu horizontale du site 
    categories_du_site = {"Accueil": "Home Page", "Officience_User": "Officience Team", "listes_badges": "Badges Collections"}
    return flask.render_template("index.html", nom_du_site = nom_du_site, categories_du_site = categories_du_site)

html_code = code(code_HTML = code_html_principale)
print(html_code)