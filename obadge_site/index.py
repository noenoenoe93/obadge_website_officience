from flask import render_template as tmp
from flask import request as rq
from flask import Flask
from flask_mysqldb import MySQL
# import flaskext.mysql
# importation de deux modules pour la barre de progression
# import alive_progress
# import time

app = Flask(__name__)

# mysql configuration
mysql = MySQL()
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = '9chqeV2qiY'
app.config['MYSQL_PASSWORD'] = 'KijTw9vZN4'
app.config['MYSQL_DB'] = '9chqeV2qiY'

# initialisation mysql
mysql.init_app(app)

@app.route("/")  # répertoire du site
def Accueil():
    return tmp("home.html")


@app.route("/inscription", methods=['POST', 'GET'])
def Inscription():
    if rq.method == "GET":
        return tmp("inscription.html")
    if rq.method == "POST":
        name = rq.form.get("name")
        password = rq.form.get("password")
        email = rq.form.get("email")
        cur = mysql.connection.cursor()  # connexion à la base de données
        cur.execute("INSERT INTO inscription VALUES (%s, %s, %s)", (name, password, email))  # exécution de la requête mysql
        cur.close()
        return tmp("inscription.html", name=name, password=password, email=email)

@app.route("/groupe")
def Team():
    return tmp("groupe.html")


@app.route("/badges")
def Badges():
    return tmp("badges.html")


@app.route("/login")
def Login():
    return tmp("login.html")