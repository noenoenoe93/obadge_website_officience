from flask_talisman import Talisman as tls
from flask import render_template as tmp, request as rq, Flask as flk, flash as fls, redirect as rdir, url_for as rlf, session as ses
# from flask_security import RegisterForm, Security as sc
from wtforms import Form as fm, StringField as stf, PasswordField as psf, EmailField as emf, SubmitField as sbm
from wtforms.validators import DataRequired as dt, Length as lg, Email as em, EqualTo as eq
from datetime import timedelta as tm
from flask_mysqldb import MySQL as msl
from flask_mail import Mail as m, Message as msg
from markupsafe import escape as esc

# partie initialisation
app = flk(__name__)
mysql = msl()
mail = m(app)
csp = {
    'default-src': 'http://127.0.0.1:5000'
}
talisman = tls(
    app, 
    content_security_policy=csp,
    frame_options = 'DENY',
    )

# session configuration
app.permanent_session_lifetime = tm(minutes=60)

# mysql configuration 
app.config["MYSQL_HOST"] = 'remotemysql.com'
app.config["MYSQL_USER"] = '9chqeV2qiY'
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_PASSWORD"] = 'KijTw9vZN4'
app.config["MYSQL_UNIX_SOCKET"] = None
app.config["MYSQL_READ_DEFAULT_FILE"] = None
app.config["MYSQL_CHARSET"] = "utf8"
app.config["MYSQL_SQL_MODE"] = None
app.config["MYSQL_AUTOCOMMIT"] = False
app.config["MYSQL_CUSTOM_OPTIONS"] = None
app.config["MYSQL_CURSORCLASS"] = None
app.config["MYSQL_USE_UNICODE"] = True
app.config["MYSQL_CONNECT_TIMEOUT"] = 20
app.config["MYSQL_DB"] = '9chqeV2qiY'
app.config["SECRET_KEY"] = '7f664d8fdeda9ebc4ffcfd82d45d2982526a16d3c74c0d3d6b15cfc7e5b0e7855621b8a37cdedb49dce67f3f3eb78446560dd9616ff10e1fe02fba7ebf004656'

# Mail Config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = "noelevanquang@gmail.com"
app.config["MAIL_PASSWORD"] = 'password'


# config sécurité
app.config["SECURITY_REDIRECT_VALIDATE_RE"] = r"^/{4,}|\\{3,}|[\s\000-\037][/\\]{2,}"

'''
# config password reset
app.config["SECURITY_RESET_PASSWORD_TEMPLATE"] = "/security/reset_password.html"
app.config["SECURITY_FORGOT_PASSWORD_TEMPLATE"] = "/security/reset_password.html"
app.config["SECURITY_POST_RESET_VIEW"] = "/"
app.config["SECURITY_RESET_PASSWORD_WITHIN"] = "1 days"
app.config["SECURITY_SEND_PASSWORD_RESET_EMAIL"] = True
app.config["SECURITY_EMAIL_SUBJECT_PASSWORD_RESET"] = "Obadge password reset"
app.config["SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE"] = "follow this link for reset your password :"
app.config["SECURITY_LOGIN_URL"] = "/security/login.html"
# app.config["SECURITY_LOGOUT_URL"] = "/logout"
app.config["SECURITY_REGISTER_URL"] = "/security/inscription.html"
app.config["SECURITY_RESET_URL"] = "/security/reset_password.html"
app.config["SECURITY_FORGOT_PASSWORD_TEMPLATE"] = "/security/forgot_password.html"
app.config["SECURITY_LOGIN_USER_TEMPLATE"] = "/security/login.html"
app.config["SECURITY_REGISTER_USER_TEMPLATE"] = "/security/inscription.html"
app.config["SECURITY_RESET_PASSWORD_TEMPLATE"] = "/security/reset_password.html"
app.config["SECURITY_EMAIL_SENDER"] = "noelevanquang@gmail.com"
'''
'''
SECURITY_DEFAULT_REMEMBER_ME
'''

@app.route("/")  # répertoire du site
def Accueil():
    return tmp("home.html")

@app.errorhandler(404) # page not found
def page_not_found(e):
    return tmp("404.html"), 404

@app.route("/security")
def Reset_password():
    return tmp("reset_password.html")

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

@app.route("/session_user") # session
def Session():
   if "name" in ses:
       return tmp("home.html")
   else:
       return tmp("fail_login.html")    

@app.route("/session_user_logout") # session
def Session_logout():
    ses.pop("name", None)
    return rdir(rlf('Login'))

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
    esc(form) # sécurité par blacklist de caractères
    if rq.method == 'POST':
        name = form.name.data
        user_email = form.email.data
        password = form.password.data
        esc(name)
        esc(user_email)
        esc(password)
        cur = mysql.connection.cursor()  # connexion à la base de données
        cur.execute("INSERT INTO login(email_user, password_user, user_name) VALUES(%s, %s, %s)", (user_email, password, name))  # exécution de la requête mysql
        dup1 = cur.execute("select * from inscription where email_user = %s",[user_email])
        dup2 = cur.execute("select * from inscription where password_user = %s",[password])
        dup3 = cur.execute("select * from inscription where user_name = %s",[name])

        # partie vérifification du mdp et de l'utilisateur dans la db
        if dup1 > 0 and dup2 > 0 and dup3 > 0:
            ses.permanent = True
            ses['name'] = name
            esc(ses) 
            cur.fetchone()
            mysql.connection.commit()
            cur.close()
            fls("Login successful")
            return rdir(rlf('Session')) # redirection avec message si infos valide

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
            lg(max=40, message="Name is too long, please try again")
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
            lg(max=40, message="Name is too long, please try again")
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
'''
class ExtendedRegisterForm(RegisterForm):
    email = em("Email : ", [dt()])

security = sc(app, reset_password_form=ExtendedRegisterForm)
'''