from flask import flash, render_template as tmp
from flask import request as rq
from flask import Flask as flk
from flask import flash as fls
from flask import redirect as rdir
from flask import url_for as rlf
from flask_mysqldb import MySQL as msl
from wtforms import Form as fm
from wtforms import StringField as stf
from wtforms import PasswordField as psf
from wtforms import validators as vld
from wtforms import EmailField as emf
# from validators import validation, RegistrationForm
# import flaskext.mysql
# importation de deux modules pour la barre de progression
# import alive_progress
# import time

app = flk(__name__)

# mysql configuration
mysql = msl()
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
    form = RegistrationForm(rq.form)
    if rq.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data
        email = form.email.data
        cur = mysql.connection.cursor()  # connexion à la base de données
        cur.execute("INSERT INTO inscription(user_name, password_user, email_user) VALUES(%s, %s, %s)", (name, password, email))  # exécution de la requête mysql
        mysql.connection.commit()
        cur.close()
        return tmp("inscription.html", form=form)
    else:
        return tmp("error.html")

@app.route("/groupe")
def Team():
    return tmp("groupe.html")


@app.route("/badges")
def Badges():
    return tmp("badges.html")


@app.route("/login")
def Login():
    return tmp("login.html")

# partie vérification
class RegistrationForm(fm):
    name = stf('name', [vld.Length(min=4, max=25)])
    password = psf('password', [vld.Length(min=6, max=100)])
    email = emf('email', [vld.Length(min=6, max=50)])