import flask
import flaskext.mysql
# importation de deux modules pour la barre de progression
# import alive_progress
# import time

app = flask.Flask(__name__)

# mysql configuration
mysql = flaskext.mysql.MySQL()
app.config['MYSQL_HOST'] = 'sql102.byethost18.com'
app.config['MYSQL_USER'] = 'b18_31066232'
app.config['MYSQL_PASSWORD'] = 'noenoenoe93100'
app.config['MYSQL_DB'] = 'b18_31066232_obadge_officience'


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

    @app.route("/badges")
    def Badges():
        return flask.render_template("badges.html")

    @app.route("/login")
    def Login():
        return flask.render_template("login.html")


html_code = code_accueil(code_HTML_principal=code_accueil)
print(html_code)
