from flask import render_template as tmp
from flask import request as rq
from flask import Flask as flk
from flask import flash as fls
from flask import redirect as rdir
from flask import url_for as rlf
from flask_mysqldb import MySQL as msl
from wtforms import Form as fm
from wtforms import StringField as stf
from wtforms import PasswordField as psf
# from wtforms import validators as vld
from wtforms import EmailField as emf
from wtforms import SubmitField as sbm
from wtforms.validators import DataRequired as dt
from wtforms.validators import Length as lg
from wtforms.validators import Email as em
from wtforms.validators import EqualTo as eq

app = flk(__name__)

# mysql configuration
mysql = msl()
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = '9chqeV2qiY'
app.config['MYSQL_PASSWORD'] = 'KijTw9vZN4'
app.config['MYSQL_DB'] = '9chqeV2qiY'
app.config['SECRET_KEY'] = 'abcdefghijklmnop'

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
        dup = cur.execute("SELECT user_name, COUNT(user_name) FROM inscription GROUP BY user_name HAVING COUNT(user_name)>1;")
        dup2 = cur.execute("SELECT email_user, COUNT(email_user) FROM inscription GROUP BY email_user HAVING COUNT(email_user)>1;")

        # partie vérifification des doublons dans la db
        if dup >= 1 or dup2 >= 1:
                cur.close()
                fls("Sorry, username or email is already taken") # redirection avec message si infos non valide
                return rdir(rlf('Fail'))
        else:
                mysql.connection.commit()
                cur.close()
                fls("Congrats you are now registered and may log in.")
                return rdir(rlf('Success')) # redirection avec message si infos valide
    return tmp("inscription.html", form=form)

@app.route("/groupe")
def Team():
    return tmp("groupe.html")

@app.route("/fail") # page de redirection signup
def Fail():
    return tmp("fail.html")

@app.route("/success_register") # page de redirection signup
def Success():
    return tmp("success_register.html") 

@app.route("/badges")
def Badges():
    return tmp("badges.html")

@app.route("/login")
def Login():
    return tmp("login.html")

# partie vérification signup
class RegistrationForm(fm):
    name = stf(
        "Name : ",
        [
            dt(message="Please enter a name"),
            lg(min=4, message="Name is too short, please try again."),
            lg(max=40, message="Name is too long, please try again"),
        ]
    )

    email = emf(
        "Email : ",
        [
            em(message="Please enter a email"),
            lg(min=4, message="Mail is too short, please try gain"),
            lg(max=40, message="Mail is too long, please try again"),
            dt()
        ]
    )

    password = psf(
        "Password : ",
        [
            dt(message="Please enter a password"),
            lg(min=4, message="Password is too short, please try again"),
            lg(max=100, message="Password is too long, please try again")
        ]
    )

    confirm_password = psf(
        "Repeat Password : ",
        [
            dt(),
            eq("password", message="Error password is different"),
            lg(min=4),
            lg(max=100)
        ]
    )
    submit = sbm("Sign Up")