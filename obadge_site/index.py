from datetime import timedelta as tm
from flask import render_template as tmp
from flask import request as rq
from flask import Flask as flk
from flask import flash as fls
from flask import redirect as rdir
from flask import url_for as rlf
from flask import session as ses
from flask_session import Session as flk_ses
from flask_mysqldb import MySQL as msl
from wtforms import Form as fm
from wtforms import StringField as stf
from wtforms import PasswordField as psf
from wtforms import EmailField as emf
from wtforms import SubmitField as sbm
from wtforms.validators import DataRequired as dt
from wtforms.validators import Length as lg
from wtforms.validators import Email as em
from wtforms.validators import EqualTo as eq

app = flk(__name__)

# session configuration
app.permanent_session_lifetime = tm(minutes=60)

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
    if "name" in ses:
        name = ses["name"]
        return f"<h1>Bienvenue : {name}</h1>"
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
        dup1 = cur.execute("SELECT user_name, COUNT(user_name) FROM inscription GROUP BY user_name HAVING COUNT(user_name)>1;")
        dup2 = cur.execute("SELECT email_user, COUNT(email_user) FROM inscription GROUP BY email_user HAVING COUNT(email_user)>1;")

        # partie vérifification des doublons dans la db
        if dup1 >= 1 or dup2 >= 1:
                cur.close()
                fls("Sorry, username or email is already taken") # redirection avec message si infos non valide
                return rdir(rlf('Fail_signup'))
        else:
                mysql.connection.commit()
                cur.close()
                fls("Congrats you are now registered and may log in.")
                return rdir(rlf('Success_signup')) # redirection avec message si infos valide
    return tmp("inscription.html", form=form)

@app.route("/groupe")
def Team():
    return tmp("groupe.html")

@app.route("/fail_signup") # page de redirection signup
def Fail_signup():
    return tmp("fail_register.html")

@app.route("/success_register") # page de redirection signup
def Success_signup():
    return tmp("success_register.html") 

@app.route("/badges")
def Badges():
    return tmp("badges.html")
'''
@app.route("/session_user") # session
def Session():
   if "name" in ses:
        name = ses["name"]
        return f"<h1>Bienvenue : {name}</h1>"
   else:
'''        

@app.route("/session_user_logout") # session
def Session_logout():
    ses.pop("name", None)
    return rdir(rlf("login"))

@app.route("/fail_login") # page de redirection login
def Fail_login():
    return tmp("fail_login.html")

@app.route("/fail_login2") # page de redirection login
def Fail_login2():
    return tmp("fail_login2.html")

@app.route("/success_login") # page de redirection login
def Success_login():
    return tmp("success_login.html")

@app.route("/login", methods=['POST', 'GET'])
def Login():
    form = LoginForm(rq.form)
    if rq.method == 'POST':
        ses.permanent = True # session permanente
        name = form.name.data
        ses['name'] = name
        user_email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()  # connexion à la base de données
        cur.execute("INSERT INTO login(email_user, password_user, user_name) VALUES(%s, %s, %s)", (user_email, password, name))  # exécution de la requête mysql
        dup1 = cur.execute("select * from inscription where email_user = %s",[user_email])
        dup2 = cur.execute("select * from inscription where password_user = %s",[password])
        dup3 = cur.execute("select * from inscription where user_name = %s",[name])

        # partie vérifification du mdp et de l'utilisateur dans la db
        if dup1 > 0 and dup2 > 0 and dup3 > 0:
            cur.fetchone()
            mysql.connection.commit()
            cur.close()
            fls("Login successful")
            return rdir(rlf('Success_login')) # redirection avec message si infos valide

        else:
            cur.close()
            fls("Error: email user does not exist, the password is incorrect or username is incorrect") # redirection avec message si infos non existante, ou non valide
            return rdir(rlf('Fail_login'))
    return tmp("login.html", form=form)

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

# partie vérification login
class LoginForm(fm):
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
    submit = sbm("Login")