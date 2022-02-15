import flask
import flaskext.mysql
import flask_mysqldb
# importation de deux modules pour la barre de progression
# import alive_progress
# import time

app = flask.Flask(__name__)

# mysql configuration
mysql = flaskext.mysql.MySQL()
app.config['MYSQL_HOST'] = 'sql102.byethost18.com'
app.config['MYSQL_USER'] = 'b18_31066232'
app.config['MYSQL_PASSWORD'] = 'noenoenoe93100'
app.config['MYSQL_DB'] = 'obadge_officience_database'


class code_accueil:
    def __init__(self, code_HTML_principal):
        self.code_HTML_principal = code_HTML_principal

    @app.route("/")  # répertoire du site
    def Accueil():
        return flask.render_template("home.html")

    @app.route("/inscription", methods=["POST", "GET"])
    def Inscription():
        if flask.request.method == "GET":
            return flask.render_template("inscription.html")
        if flask.request.method == "POST":
            name = flask.request.form.get("name")
            password = flask.request.form.get("password")
            email = flask.request.form.get("email")
            cur = flask_mysqldb.MySQL.connection.cursor() # connexion à la base de données
            flask_mysqldb.MySQL.connection.execute("INSERT INTO inscription VALUES (%s, %s, %s)",(name, password, email))  # exécution de la requête mysql
            flask_mysqldb.MySQL.connection.cursor.close()
            return flask.render_template("inscription.html", name=name, password=password, email=email)

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
